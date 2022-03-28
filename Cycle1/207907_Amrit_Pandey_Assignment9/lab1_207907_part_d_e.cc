// author: Amrit Pandey, 207907, MCA Year 2
// date: 28/03/2022
// Cycle 1 - Lab 1
 
#include <fstream>
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/network-module.h"
#include "ns3/flow-monitor-module.h"
 
using namespace ns3;
using namespace std;
 
int main(int argc, char* argv[])
{
  double lat = 4.0;
  cout << "Max Packets = 2" << endl;
  cout << "Latency = " << lat << endl;
  cout << "Interval = 1.0" << endl;

  Time::SetResolution(Time::NS);
  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);
 
  NodeContainer nodes;
  nodes.Create(2);
 
  PointToPointHelper p2p;
  p2p.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
  p2p.SetChannelAttribute("Delay", TimeValue(MilliSeconds(lat)));
 
  NetDeviceContainer devices;
  devices = p2p.Install(nodes);
 
  InternetStackHelper internet;
  internet.Install(nodes);
 
  Ipv4AddressHelper ipv4;
  ipv4.SetBase("12.0.1.0", "255.255.255.0");
 
  Ipv4InterfaceContainer interface;
  interface = ipv4.Assign(devices);
 
  int port1 = 8080;
  int port2 = 8000;
  UdpEchoServerHelper server1(port1);
  UdpEchoServerHelper server2(port2);
 
  UdpEchoClientHelper client1(interface.GetAddress(0), port1);
  client1.SetAttribute("MaxPackets", UintegerValue(1));
  client1.SetAttribute("Interval", TimeValue(Seconds(1.0)));
  client1.SetAttribute("PacketSize", UintegerValue(512));

  UdpEchoClientHelper client2(interface.GetAddress(0), port2);
  client2.SetAttribute("MaxPackets", UintegerValue(1));
  client2.SetAttribute("Interval", TimeValue(Seconds(1.0)));
  client2.SetAttribute("PacketSize", UintegerValue(512));
 
  ApplicationContainer serverApps1, serverApps2, clientApps1, clientApps2;
 
  serverApps1 = server1.Install(nodes.Get(0));
  serverApps1.Start(Seconds(0.0));
  serverApps1.Stop(Seconds(10.0));
 
  serverApps2 = server2.Install(nodes.Get(0));
  serverApps2.Start(Seconds(0.0));
  serverApps2.Stop(Seconds(10.0));
 
  clientApps1 = client1.Install(nodes.Get(1));
  clientApps1.Start(Seconds(0.0));
  clientApps1.Stop(Seconds(10.0));
 
  clientApps2 = client2.Install(nodes.Get(1));
  clientApps2.Start(Seconds(0.0));
  clientApps2.Stop(Seconds(10.0));
 
  AsciiTraceHelper ascii;
  p2p.EnableAscii(ascii.CreateFileStream ("lab1-207907-part-d-e.tr"), devices);
  p2p.EnablePcap("lab1-207907-part-d-e", devices, false);

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();

  Simulator::Stop(Seconds(11.0));
  Simulator::Run();

  monitor->CheckForLostPackets();

  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats ();
  for (std::map<FlowId, FlowMonitor::FlowStats>::const_iterator i = stats.begin (); i != stats.end (); ++i)
  {
    Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (i->first);
      if ((t.sourceAddress=="12.0.1.1" && t.destinationAddress == "12.0.1.2"))
      {
          std::cout << "Flow " << i->first  << " (" << t.sourceAddress << " -> " << t.destinationAddress << ")\n";
          std::cout << "  Tx Bytes:   " << i->second.txBytes << "\n";
          std::cout << "  Rx Bytes:   " << i->second.rxBytes << "\n";
          std::cout << "  Throughput: " << i->second.rxBytes * 8.0 / (i->second.timeLastRxPacket.GetSeconds() - i->second.timeFirstTxPacket.GetSeconds())/1024/1024  << " Mbps\n";
      }
   }

  monitor->SerializeToXmlFile("lab1-207907-part-a-b.flowmon", true, true);

  Simulator::Destroy();
 
  return 0;
}

