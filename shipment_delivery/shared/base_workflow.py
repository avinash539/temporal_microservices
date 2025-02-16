from datetime import timedelta
from typing import Any, Callable, Dict, Optional
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError, ApplicationError

@workflow.defn
class RetryableWorkflow:
    def __init__(self):
        self._resume_flags: Dict[str, bool] = {}
        
    @workflow.signal
    async def resume_service(self, service_name: str) -> None:
        """Signal to resume a paused service"""
        self._resume_flags[service_name] = True
        
    @workflow.run
    async def run(self, *args: Any, **kwargs: Any) -> Any:
        """
        Base run method that must be overridden by child classes.
        This is required by Temporal but should never be called directly on the base class.
        """
        raise NotImplementedError("RetryableWorkflow is a base class and cannot be run directly")
        
    async def execute_with_retry_and_pause(
        self,
        activity_name: str,
        service_name: str,
        input_data: Dict[str, Any],
        task_queue: str,
        max_attempts: int = 3,
        timeout: timedelta = timedelta(minutes=5),
    ) -> Dict[str, Any]:
        """
        Execute an activity with retry and pause capability.
        If the activity fails after max_attempts, it will pause and wait for a resume signal.
        """
        self._resume_flags.setdefault(service_name, False)
        
        while True:
            try:
                # Configure retry policy
                retry_policy = RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_interval=timedelta(seconds=10),
                    maximum_attempts=max_attempts,
                    non_retryable_error_types=["NotRetryableError"]
                )
                
                # Execute the activity with retry policy
                result = await workflow.execute_activity(
                    activity_name,
                    input_data,
                    start_to_close_timeout=timeout,
                    retry_policy=retry_policy,
                    task_queue=task_queue,
                )
                return result
                
            except ActivityError as e:
                workflow.logger.error(f"{service_name} failed after {max_attempts} attempts. Pausing workflow.")
                # Reset the resume flag
                self._resume_flags[service_name] = False
                # Wait for the resume signal
                await workflow.wait_condition(lambda: self._resume_flags[service_name])
                workflow.logger.info(f"Resuming {service_name} after pause")
                # Continue the loop to retry the activity
                continue 