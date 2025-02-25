import { Context } from '@temporalio/activity';

interface OrderData {
  orderId: string;
  partnerId?: string;
  orderDetails: Record<string, any>;
}

interface NetworkPartner {
  partnerId: string;
  name: string;
  config: Record<string, any>;
  priority: number;
}

// Available delivery partners
const DELIVERY_PARTNERS: NetworkPartner[] = [
  {
    partnerId: 'delhivery',
    name: 'Delhivery',
    config: {
      apiEndpoint: 'https://api.delhivery.com',
      region: 'INDIA'
    },
    priority: 1
  },
  {
    partnerId: 'ekart',
    name: 'Ekart',
    config: {
      apiEndpoint: 'https://api.ekart.com',
      region: 'INDIA'
    },
    priority: 2
  },
  {
    partnerId: 'ecom-express',
    name: 'Ecom Express',
    config: {
      apiEndpoint: 'https://api.ecomexpress.com',
      region: 'INDIA'
    },
    priority: 3
  },
  {
    partnerId: 'blue-dart',
    name: 'Blue Dart',
    config: {
      apiEndpoint: 'https://api.bluedart.com',
      region: 'INDIA'
    },
    priority: 4
  },
  {
    partnerId: 'xpressbees',
    name: 'Xpressbees',
    config: {
      apiEndpoint: 'https://api.xpressbees.com',
      region: 'INDIA'
    },
    priority: 5
  }
];

// Find eligible partners based on order criteria
export async function findEligiblePartner(orderData: OrderData): Promise<NetworkPartner[]> {
  Context.current().heartbeat('Evaluating partners...');

  // Simulating partner evaluation delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  // In a real implementation, this would filter partners based on various criteria
  // like delivery region, order type, cost, etc.
  const eligiblePartners = DELIVERY_PARTNERS
    .filter(partner => {
      // Add your eligibility criteria here
      // For demo, we'll return top 3 partners by priority
      return partner.priority <= 3;
    })
    .sort((a, b) => a.priority - b.priority);

  if (eligiblePartners.length === 0) {
    throw new Error('No eligible partners found for the order');
  }

  return eligiblePartners;
}