#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Pretty;
use Data::Dumper;
use LWP::UserAgent;
use Time::HiRes qw(gettimeofday);
print header;
print start_html(-title=>"MPMon", -style => {-src => 'css/main.css'});
my ($socket, $status);
open (my $fh, "<", "SVCs");
while (my $line = <$fh>){
  my @list=split(', ',$line);
  $socket =
    IO::Socket::INET->new( PeerAddr	=> $list[0],
    PeerPort	=> $list[1],
    Proto	=> 'tcp',
    Type	=>  SOCK_STREAM);
  if ($socket){
    $status .= "<span class='goodstat'>".$list[0].":".$list[1]."</span>";
    close ($socket);
  }else{
    $status .= $list[0].":".$list[2].":".=  "<b style='color:red'>&or;</b>";
  }
  $status .= "<br />\n";
}
print "<h2 style='text-align:center'>Los Angeles</h2>";
print "<div style='width:50%;float:left'>";
print   "<h3>Services</h3>";
print $status;
print "</div>";
print "<div style='width:50%;float:right'>";
print   "<h3>Sites</h3>";
open (my $fh, "<", "URLs");
while (my $line = <$fh>) {
  my @list = split(',', $line);
  my $ua = LWP::UserAgent->new;
  $ua->timeout(5);
  for my $webhost (@list[0]){
    my $start = gettimeofday ;
    my $response = $ua->get("http://$webhost");
    my $stop = gettimeofday;
    my $gwebhost="<a href='http://$webhost' class='goodstat'>$webhost</a>";
    my $bwebhost="<a href='http://$webhost' class='badstat'>$webhost</a>";
    chomp ($list[1]);
    my $match = index(Dumper($response), $list[1]);
    if ($response->is_success) {
      if ($match>-1) {
        print "$gwebhost:";
        printf ("<span class='goodstat'>%1.1fs</span>",($stop - $start));
        print "<br />\n"; 
      } else { print "$bwebhost <b class='badstat'>!~$list[1]</b><br />\n"; }
    } else { print "$bwebhost is <b class='badstat'>&or;</b>!<br />\n"; }; 
  } 
}
print "</div>";
print end_html;
