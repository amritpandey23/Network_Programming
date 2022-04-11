// author: Amrit Pandey, 207907, MCA Year 2
// date: 11 April 2022

/* 
Build an Client and Server Echo Application by designing Bus Network Topology (Figure-2) Using Python and capture ECHO packets transmitted from Node-1 to Node-4 and Analyze it using Wireshark
*/

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/csma-module.h"
#include "ns3/ipv4-global-routing-helper.h"

using namespace ns3;
NS_LOG_COMPONENT_DEFINE("Cycle 1, Assignment 2 -- Lab 2");

int main(int argc, char* argv[])
{
	LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);
	LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);

	uint8_t udpServerPort = 9;
	
	NodeContainer p2pnodes;
	p2pnodes.Create(2);
	
	PointToPointHelper p2p;
	p2p.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
	p2p.SetChannelAttribute("Delay", StringValue("2ms"));
	
	NetDeviceContainer p2pDevices;
	p2pDevices = p2p.Install(p2pnodes);
	
	NodeContainer csmaNodes;
	csmaNodes.Add(p2pnodes.Get(1));
	csmaNodes.Create(3);
	
	CsmaHelper csma;
	csma.SetChannelAttribute("DataRate", StringValue("5Mbps"));
	csma.SetChannelAttribute("Delay", TimeValue(NanoSeconds(6000)));
	
	NetDeviceContainer csmaDevices;
	csmaDevices = csma.Install(csmaNodes);
	
	InternetStackHelper internet;
	internet.Install(p2pnodes.Get(0));
	internet.Install(csmaNodes);
	
	Ipv4AddressHelper address;
	
	address.SetBase("10.1.1.0", "255.255.255.0");
	Ipv4InterfaceContainer p2pInterface;
	p2pInterface = address.Assign(p2pDevices);
	
	address.SetBase("10.1.2.0", "255.255.255.0");
	Ipv4InterfaceContainer csmaInterface;
	csmaInterface = address.Assign(csmaDevices);
	
	UdpEchoServerHelper echoServer(udpServerPort);
	
	ApplicationContainer serverApps = echoServer.Install(csmaNodes.Get(3));
	serverApps.Start(Seconds(1.0));
	serverApps.Stop(Seconds(10.0));

	UdpEchoClientHelper echoClient(csmaInterface.GetAddress(3), udpServerPort);
	echoClient.SetAttribute("MaxPackets", UintegerValue(1));
	echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
	echoClient.SetAttribute("PacketSize", UintegerValue(512));

	ApplicationContainer clientApps = echoClient.Install(p2pnodes.Get(0));
  clientApps.Start(Seconds(2.0));
  clientApps.Stop(Seconds(10.0));

  // populating global routing table
  // for the given topology
  Ipv4GlobalRoutingHelper::PopulateRoutingTables();

  p2p.EnablePcap("lab2", p2pDevices.Get(1));
  csma.EnablePcap("lab2", csmaDevices.Get(3));
	
	Simulator::Run();
	Simulator::Destroy();
	
	return 0;
}

