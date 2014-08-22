#!/opt/local/bin/perl
use strict;
use warnings;
open (my $fh, "<", "SERVICEs");
while (my $line = <$fh>){
my @list=split(',',$line);
print $list[1].$list[2]."\n";
#  }
}
