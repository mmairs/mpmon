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
print start_html(-style => {-src => 'css/main.css'});
my $serprobs=0;
my $urlprobs=0;
my ($socket, $status);
open (my $fh, "<", "SERVICEs");
while (my $line = <$fh>){
  my @list=split(', ',$line);
  $socket = IO::Socket::INET->new(
    PeerAddr     => $list[1],
    PeerPort    => $list[2],
    Proto       => 'tcp',
    Type        => SOCK_STREAM,
    Timeout     => 5);
  if ($socket){
    close ($socket);
  }else{
    $status .= $list[0]." port ".$list[1]." is ".= "<b class='badstat'>CLOSED</b><br />";
    $serprobs=1;
  }
}
print "<h2 style='text-align:center'>Boston</h2>";
print "<div class='left'>";
print "  <h3>Services</h3>";
($serprobs==1)?(print $status):(print "No Problems");
print "</div>";
print "<div class='right'>";
print "  <h3>Sites</h3>";
open (my $fh, "<", "URLs");
my $urlprobs=0;
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
      } else { print "$bwebhost <b class='badstat'>!~$list[1]</b><br />\n";
               $urlprobs=1; }
    } else { print "$bwebhost is <b class='badstat'>&or;</b>!<br />\n";
             $urlprobs=1; }
  }
} ($urlprobs==1)?():(print "No Problems"); 
print "</div>";
print end_html;
