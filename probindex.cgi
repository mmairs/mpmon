#!/usr/bin/perl
use strict;
use warnings;
use IO::Socket;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Pretty;
use LWP::UserAgent;
print header;
print start_html(-title=>"MPMon", -style => {-src => 'css/main.css'}, -meta => {
 'keywords' => 'perl, massively, parallel, monitor',
 'description' => 'Matt\'s Perl Monitor'});
print "<div class='header'>";
print "<a class='mpmon' href='http://www.mpmon.com'><span style='color:red'>M</span><span style='color:green'>P</span><span style='color:blue'>M</span>on Problems</a>";
print "</div>";
my $serprobs=0;
my $urlprobs=0;
my ($socket, $status);
open (my $fh, "<", "SERVICEs");
while (my $line = <$fh>){
  my @list=split(', ',$line);
  $socket =
    IO::Socket::INET->new( PeerAddr	=> $list[1],
    PeerPort	=> $list[2],
    Proto	=> 'tcp',
    Type	=> SOCK_STREAM,
    Timeout	=> 5);
  if ($socket){
    close ($socket);
  }else{
    $status .= $list[0]." port ".$list[2]." is ".= "<b class='badstat'>CLOSED</b><br />";
    $serprobs=1;
  }
}
print "<div class='fleft'>";
print   "<div class='tab1'>";
print   "<a href='probindex.cgi'>Problems</a>";
print   "</div>";
print   "<div class='tab2'>";
print   "<a href='index.cgi'>Overview</a>";
print   "</div>";
print   "<div class='tab3'>";
print   "<a href='https://github.com/mmairs/mpmon'>Code</a>";
print   "</div>";
print "</div>";
print "<div class='left'>";
print   "<h2 style='text-align:center'>New York</h2>";
print     "<h3>Services</h3>";
($serprobs==1)?(print $status):(print "No Problems");
print     "<h3>Sites</h3>";
open (my $fh, "<", "URLs");
my $line = <$fh>;
my @line_array = split(',', $line);
my $ua = LWP::UserAgent->new;
$ua->timeout(5);
for my $webhost (@line_array){
  my $response = $ua->get("http://$webhost");
  if ($response->is_success) {
  } else {
    print "URL $webhost is <b class='badstat'>not responding</b>.<p />\n";
    $urlprobs=1;
  }
}
($urlprobs==1)?():(print "No Problems");
print "</div>"; #oleft
print "<div class='middle'>";
print "<div class='ileft'>";
print   "<iframe src='http://z0mb135.com/mpmon/node/problems.cgi' frameborder='0' width='100%' height='1000px'></iframe>";
print "</div>";
print "<div class='iright'>";
print   "<iframe src='http://max.mairs.net/mpmon/node/problems.cgi' frameborder='0' width='100%' height='1000px'>";
print "</iframe>";
print "</div>";
print "</div>";
print "<div class='right'>";
print   "<iframe src='http://no.justicejust.us/p.php' frameborder='0' width='100%' height='1000px'>";
print "</iframe>";
print "</div>";
print "<div class='v'>";
print "<a href='http://validator.w3.org/check?uri=referer'><img src='http://www.w3.org/Icons/valid-xhtml10' alt='Valid XHTML 1.0 Transitional' height='31' width='88' /></a>";
print "</div>";
print end_html;
exit;
