#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Pretty;
use LWP::UserAgent;
use Time::HiRes qw(gettimeofday);
print header;
print start_html(-title=>"MPMon", -style => {-src => '/css/main.css'});
my ($socket, $status);
open (my $fh, "<", "SERVICEs");
while (my $line = <$fh>){
  my @list=split(', ',$line);
  $socket =
    IO::Socket::INET->new( PeerAddr	=> $list[1],
    PeerPort	=> $list[2],
    Proto	=> 'tcp',
    Type	=>  SOCK_STREAM);
  if ($socket){
    $status .= $list[0]." port ".$list[2]." is ".=  "<b style='color:green'>LISTENING</b>";
    close ($socket);
  }else{
    $status .= $list[0]." port ".$list[2]." is ".=  "<b style='color:red'>CLOSED</b>";
  }
  $status .= "<br />\n";
}
print "<h2 style='text-align:center'>West Coast US</h2>";
print "<div style='width:50%;float:left'>";
print   "<h3>Services</h3>";
print $status;
print "</div>";
print "<div style='width:50%;float:right'>";
print   "<h3>Sites</h3>";
open (my $fh, "<", "URLs");
my $line = <$fh>;
my @line_array = split(/\s+/, $line);
my $ua = LWP::UserAgent->new;
$ua->timeout(5);
for my $webhost (@line_array){
  chop($webhost);
  my $start = gettimeofday ;
  my $response = $ua->get("$webhost");
  my $stop = gettimeofday ;
  if ($response->is_success)  {
    print "$webhost  <b style='color:green'>responds</b> in ";
    printf ("%1.3f",($stop - $start));
    print "s<br />\n"; }
  else { print "$webhost is <b class='badstat'>not responding</b>.<br />\n"; }
}
print "</div>";
print end_html;
