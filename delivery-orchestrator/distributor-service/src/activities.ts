import { ApplicationFailure, Context } from '@temporalio/activity';

export interface OrderData {
  orderId: string;
  partnerId?: string;
  orderDetails: {
    items: Array<{ name: string; quantity: number }>;
    deliveryAddress: string;
  };
}

export interface Partner {
  partnerId: string;
  name: string;
  config: {
    apiEndpoint: string;
    region: string;
  };
  priority: number;
}

export interface DistributionResult {
  success: boolean;
  partnerId: string;
  partnerName: string;
  orderId: string;
  attemptNumber: number;
  totalAttempts: number;
}

export async function attemptPartnerDistribution(
  orderData: OrderData,
  partner: Partner,
  attemptNumber: number,
  totalPartners: number,
  retryAttempt: number
): Promise<DistributionResult> {
  const activity = Context.current();

  activity.heartbeat(
    `Partner ${attemptNumber}/${totalPartners} (${partner.name}), Retry ${retryAttempt}/3: Starting distribution attempt`
  );

  // Transform order data according to partner's requirements
  const transformedOrder = {
    reference_id: orderData.orderId,
    partner_id: partner.partnerId,
    delivery_details: {
      ...orderData.orderDetails,
      partner_config: partner.config
    }
  };

  // Send order to partner
  activity.heartbeat(`Partner ${partner.name}, Retry ${retryAttempt}: Sending order to API endpoint`);
  if (['delhivery'].includes(partner.partnerId)) {
    throw new ApplicationFailure(`Distribution failed for partner ${partner.name}`);
  }

  activity.heartbeat(`Partner ${partner.name}, Retry ${retryAttempt}: Order successfully distributed`);

  return {
    success: true,
    partnerId: partner.partnerId,
    partnerName: partner.name,
    orderId: orderData.orderId,
    attemptNumber,
    totalAttempts: totalPartners
  };
}

export async function distributeOrder(orderData: OrderData, partners: Partner[]): Promise<DistributionResult> {
  const activity = Context.current();
  activity.heartbeat('Starting order distribution...');

  // If a specific partner is requested, use only that partner
  if (orderData.partnerId) {
    const requestedPartner = partners.find(p => p.partnerId === orderData.partnerId);
    if (!requestedPartner) {
      throw new Error(`Requested partner ${orderData.partnerId} not found`);
    }
    partners = [requestedPartner];
  }

  // This activity now just validates the input and throws an error if no partners are available
  if (partners.length === 0) {
    throw new Error('No partners available to process the order');
  }

  activity.heartbeat(`Found ${partners.length} eligible partners for distribution`);

  // The actual distribution attempts will be handled by the workflow
  throw new Error('This activity should not be called directly. Use attemptPartnerDistribution instead.');
}