#!/usr/bin/perl
#Props Kirk Brown http://perl.about.com/od/appliedprogramming/ss/servicemonitor_5.htm and Thomas Nooning http://www.techrepublic.com/article/solutionbase-set-up-customized-network-monitoring-with-perl
use strict;
use warnings;
use IO::Socket;
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Pretty;
use LWP::UserAgent;
print header(-Refresh => "300;url=http://www.mpmon.com");
print start_html(-title=>"MPMon", -style => {-src => 'css/main.css'}, -meta => {
 'keywords' => 'perl, massively, parallel, monitor',
 'description' => 'Matt\'s Perl Monitor'});
print "<div class='header'>";
print "<a class='mpmon' href='http://www.mpmon.com'><span style='color:red'>M</span><span style='color:green'>P</span><span style='color:blue'>M</span>on Overview</a>";
print "</div>";
print "<div class='fleft'>";
print   "<div class='tab1'>";
print   "<a href='index.cgi'>Overview</a>";
print   "</div>";
print   "<div class='tab2'>";
print   "<a href='probindex.cgi'>Problems</a>";
print   "</div>";
print   "<div class='tab3'>";
print   "<a href='https://github.com/mmairs/mpmon'>Code</a>";
print   "</div>";
print "</div>";
print "<div class='left'>";
print   "<iframe src='http://www.mpmon.com/pynode/monitor.py' frameborder='0' width='100%' height='450px'></iframe>";
print "</div>";
print "<div class='middle'>";
print   "<iframe src='http://www.minusorpl.us/node/overview.cgi' frameborder='0' width='100%' height='450px'></iframe>";
print "</div>";
print "<div class='right'>";
print   "<iframe src='http://mpmon.mairs.net/node/overview.cgi' frameborder='0' width='100%' height='450px'></iframe>";
print "</div>";
print "<div class='v'>";
print "<a href='http://validator.w3.org/check?uri=referer'><img src='http://www.w3.org/Icons/valid-xhtml10' alt='Valid XHTML 1.0 Transitional' height='31' width='88' /></a>";
print "</div>";
print "<div style='position:absolute; bottom:0;right:0'>Last Refreshed: ".`date`."</div>";
print end_html;
exit;
