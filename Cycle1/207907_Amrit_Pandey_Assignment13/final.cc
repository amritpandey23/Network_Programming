#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"


using namespace ns3;
class MyApp : public Application 
 {
 public:
 
   MyApp ();
   virtual ~MyApp();
 
   void Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate);
 
 private:
   virtual void StartApplication (void);
   virtual void StopApplication (void);
 
   void ScheduleTx (void);
   void SendPacket (void);
 
   Ptr<Socket>     m_socket;
   Address         m_peer;
   uint32_t        m_packetSize;
   uint32_t        m_nPackets;
   DataRate        m_dataRate;
   EventId         m_sendEvent;
   bool            m_running;
   uint32_t        m_packetsSent;
 };
 
 MyApp::MyApp ()
   : m_socket (0), 
     m_peer (), 
     m_packetSize (0), 
     m_nPackets (0), 
     m_dataRate (0), 
     m_sendEvent (), 
     m_running (false), 
     m_packetsSent (0)
 {
 }
 
 MyApp::~MyApp()
 {
   m_socket = 0;
 }
 
 void
 MyApp::Setup (Ptr<Socket> socket, Address address, uint32_t packetSize, uint32_t nPackets, DataRate dataRate)
 {
   m_socket = socket;
   m_peer = address;
   m_packetSize = packetSize;
   m_nPackets = nPackets;
   m_dataRate = dataRate;
 }
 
 void
 MyApp::StartApplication (void)
 {
   m_running = true;
   m_packetsSent = 0;
   m_socket->Bind ();
   m_socket->Connect (m_peer);
   SendPacket ();
 }
 
 void 
 MyApp::StopApplication (void)
 {
   m_running = false;
 
   if (m_sendEvent.IsRunning ())
     {
       Simulator::Cancel (m_sendEvent);
     }
 
   if (m_socket)
     {
       m_socket->Close ();
     }
 }
 
 void 
 MyApp::SendPacket (void)
 {
   Ptr<Packet> packet = Create<Packet> (m_packetSize);
   m_socket->Send (packet);
 
   if (++m_packetsSent < m_nPackets)
     {
       ScheduleTx ();
     }
 }
 
 void 
 MyApp::ScheduleTx (void)
 {
   if (m_running)
     {
       Time tNext (Seconds (m_packetSize * 8 / static_cast<double> (m_dataRate.GetBitRate ())));
       m_sendEvent = Simulator::Schedule (tNext, &MyApp::SendPacket, this);
     }
 }
 
 static void
 CwndChange (uint32_t oldCwnd, uint32_t newCwnd)
 {
   NS_LOG_UNCOND (Simulator::Now ().GetSeconds () << "\t" << newCwnd);
 }
 
 static void
 RxDrop (Ptr<const Packet> p)
 {
   NS_LOG_UNCOND ("RxDrop at " << Simulator::Now ().GetSeconds ());
 }

int main(int argc, char *argv[]) {
  /*
  0 -----                  ----- 2
      |                   |
      ---- 4 ------ 5 ----
      |                   |
  1 ----                  ----- 3

  0 - 2 (tcp)
  1 - 2
  1 - 3
  */

  NodeContainer nodes;
  nodes.Create(6);

  PointToPointHelper p2p;
  p2p.SetChannelAttribute("Delay", StringValue("2ms"));
  p2p.SetDeviceAttribute("DataRate", StringValue("5Mbps"));

  NetDeviceContainer d04 = p2p.Install(nodes.Get(0), nodes.Get(4));
  NetDeviceContainer d14 = p2p.Install(nodes.Get(1), nodes.Get(4));
  NetDeviceContainer d25 = p2p.Install(nodes.Get(2), nodes.Get(5));
  NetDeviceContainer d35 = p2p.Install(nodes.Get(3), nodes.Get(5));
  NetDeviceContainer d45 = p2p.Install(nodes.Get(4), nodes.Get(5));
  NetDeviceContainer d02 = p2p.Install(nodes.Get(0), nodes.Get(2));
  NetDeviceContainer d12 = p2p.Install(nodes.Get(1), nodes.Get(2));
  NetDeviceContainer d13 = p2p.Install(nodes.Get(1), nodes.Get(3));

  InternetStackHelper internet;
  internet.Install(nodes);

  Ipv4AddressHelper address;

  address.SetBase("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i04 = address.Assign(d04);

  address.SetBase("10.1.2.0", "255.255.255.0");
  Ipv4InterfaceContainer i14 = address.Assign(d14);

  address.SetBase("10.1.3.0", "255.255.255.0");
  Ipv4InterfaceContainer i25 = address.Assign(d25);

  address.SetBase("10.1.4.0", "255.255.255.0");
  Ipv4InterfaceContainer i35 = address.Assign(d35);

  address.SetBase("10.1.5.0", "255.255.255.0");
  Ipv4InterfaceContainer i45 = address.Assign(d45);

  address.SetBase("10.1.6.0", "255.255.255.0");
  Ipv4InterfaceContainer i02 = address.Assign(d02);

  address.SetBase("10.1.7.0", "255.255.255.0");
  Ipv4InterfaceContainer i12 = address.Assign(d12);

  address.SetBase("10.1.8.0", "255.255.255.0");
  Ipv4InterfaceContainer i13 = address.Assign(d13);

  Ipv4GlobalRoutingHelper::PopulateRoutingTables();

  // TCP connfection from n1 to n3
  uint16_t sinkPort = 8080;
  Address sinkAddress(
      InetSocketAddress(i02.GetAddress(1), sinkPort)); // interface of n3
  PacketSinkHelper packetSinkHelper(
      "ns3::TcpSocketFactory",
      InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
  ApplicationContainer sinkApps =
      packetSinkHelper.Install(nodes.Get(2)); // n3 as sink
  sinkApps.Start(Seconds(0.));
  sinkApps.Stop(Seconds(100.));

  Ptr<Socket> ns3TcpSocket = Socket::CreateSocket(
      nodes.Get(0), TcpSocketFactory::GetTypeId()); // source at n1

  // Trace Congestion window
  ns3TcpSocket->TraceConnectWithoutContext("CongestionWindow",
                                           MakeCallback(&CwndChange));

  // Create TCP application at n1
  Ptr<MyApp> app = CreateObject<MyApp>();
  app->Setup(ns3TcpSocket, sinkAddress, 1040, 100000, DataRate("250Kbps"));
  nodes.Get(0)->AddApplication(app);
  app->SetStartTime(Seconds(1.));
  app->SetStopTime(Seconds(100.));

  // TCP connfection from n1 to n2
  uint16_t sinkPort = 8080;
  Address sinkAddress(
      InetSocketAddress(i12.GetAddress(2), sinkPort)); // interface of n3
  PacketSinkHelper packetSinkHelper(
      "ns3::TcpSocketFactory",
      InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
  ApplicationContainer sinkApps =
      packetSinkHelper.Install(nodes.Get(2)); // n3 as sink
  sinkApps.Start(Seconds(0.));
  sinkApps.Stop(Seconds(100.));

  Ptr<Socket> ns3TcpSocket = Socket::CreateSocket(
      nodes.Get(1), TcpSocketFactory::GetTypeId()); // source at n1

  // Trace Congestion window
  ns3TcpSocket->TraceConnectWithoutContext("CongestionWindow",
                                           MakeCallback(&CwndChange));

  // Create TCP application at n1
  Ptr<MyApp> app = CreateObject<MyApp>();
  app->Setup(ns3TcpSocket, sinkAddress, 1040, 100000, DataRate("250Kbps"));
  nodes.Get(1)->AddApplication(app);
  app->SetStartTime(Seconds(1.));
  app->SetStopTime(Seconds(100.));


  // TCP connfection from n1 to n3
  uint16_t sinkPort = 8080;
  Address sinkAddress(
      InetSocketAddress(i13.GetAddress(1), sinkPort)); // interface of n3
  PacketSinkHelper packetSinkHelper(
      "ns3::TcpSocketFactory",
      InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
  ApplicationContainer sinkApps =
      packetSinkHelper.Install(nodes.Get(3)); // n3 as sink
  sinkApps.Start(Seconds(0.));
  sinkApps.Stop(Seconds(100.));

  Ptr<Socket> ns3TcpSocket = Socket::CreateSocket(
      nodes.Get(1), TcpSocketFactory::GetTypeId()); // source at n1

  // Trace Congestion window
  ns3TcpSocket->TraceConnectWithoutContext("CongestionWindow",
                                           MakeCallback(&CwndChange));

  // Create TCP application at n1
  Ptr<MyApp> app = CreateObject<MyApp>();
  app->Setup(ns3TcpSocket, sinkAddress, 1040, 100000, DataRate("250Kbps"));
  nodes.Get(1)->AddApplication(app);
  app->SetStartTime(Seconds(1.));
  app->SetStopTime(Seconds(100.));


  Simulator::Run();
  Simulator::Stop(Seconds(100.0));
  Simulator::Destroy();
  return 0;
}
