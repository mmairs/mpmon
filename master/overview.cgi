#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use LWP::UserAgent;
use Time::HiRes qw(gettimeofday);
print header;
print start_html(-style=>{-code=>"body {font-size:12px;font-family:Helvetica}"});
print "<h2 style='text-align:center'>East Coast US</h2>";
my ($socket, $status);
open (my $fh, "<", "SERVICEs");
while (my $line = <$fh>){
  my @list=split(', ',$line);
  $socket =
    IO::Socket::INET->new( PeerAddr	=> $list[1],
    PeerPort	=> $list[2],
    Proto	=> 'tcp',
    Type	=> SOCK_STREAM,
    Timeout	=> 3);
  if ($socket){
    $status .= $list[0]." port ".$list[2]." is ".=  "<b style='color:green'>LISTENING</b>";
    close ($socket);
  }else{
    $status .= $list[0]." port ".$list[2]." is ".=  "<b style='color:red'>CLOSED</b>";
  }
  $status .= "<br />\n";
}
print "<div style='width:50%;float:left'>";
print "<h3>Services</h3>";
print $status;
print "</div>";
print "<div style='float:right;width:50%'>";
print "<h3>Sites</h3>";
open (my $fh, "<", "URLs");
my $line = <$fh>;
my @line_array = split(/\s+/, $line);
my $ua = LWP::UserAgent->new;
$ua->timeout(15);
for my $webhost (@line_array){
  chop($webhost);
  my $start = gettimeofday ;
  my $response = $ua->get("$webhost");
  my $stop = gettimeofday ;
  if ($response->is_success) {
    print "$webhost  <b style='color:green'>responds</b> in ";
    printf ("%1.3f",($stop - $start));
    print "s<br />\n"; }
  else { print "$webhost is <b style='color:red'>not responding</b>.<br />\n"; }
}
print "</div>";
print end_html;
exit;
