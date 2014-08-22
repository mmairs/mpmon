#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Pretty;
use LWP::UserAgent;
print header;
print start_html(-style => {-src => '/css/main.css'});
my $serprobs=0;
my $urlprobs=0;
my ($socket, $status);
open (my $fh, "<", "SERVICEs");
while (my $line = <$fh>){
  my @list=split(', ',$line);
  $socket =
    IO::Socket::INET->new( PeerAddr     => $list[1],
    PeerPort    => $list[2],
    Proto       => 'tcp',
    Type        => SOCK_STREAM,
    Timeout     => 5);
  if ($socket){
    close ($socket);
  }else{
    $status .= $list[0]." port ".$list[2]." is ".= "<b class='badstat'>CLOSED</b><br />";
    $serprobs=1;
  }
}
print "<h2 style='text-align:center'>East Coast US</h2>";
print "<div class='left'>";
print "  <h3>Services</h3>";
($serprobs==1)?(print $status):(print "No Problems");
print "</div>";
print "<div class='right'>";
print "  <h3>Sites</h3>";
open (my $fh, "<", "URLs");
my $line = <$fh>;
my @line_array = split(/\s+/, $line);
my $ua = LWP::UserAgent->new;
$ua->timeout(5);
for my $webhost (@line_array){
  chop($webhost);
  my $response = $ua->get("$webhost");
  if ($response->is_success) { }
  else {
    print "URL $webhost is <b class='badstat'>not responding</b>.<p />\n";
    $urlprobs=1;
  }
}
($urlprobs==1)?():(print "No Problems");
print "  </div>";
print "</div>";
print end_html;
exit;

