#!/usr/bin/perl
#
#    FreeS/WAN IPSEC VPN Configuration Webmin Module
#    Copyright (C) 2000-2001 by Tim Niemueller <tim@niemueller.de>
#    http://www.niemueller.de/webmin/modules/freeswan/
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    Created  : 16.09.2000


require "./freeswan-lib.pl";
@pc=&parse_config();
my $config=&get_section(\@pc, 'config', 'setup');

&header($text{'eifcs_title'}, undef, "eifcs", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>";

print "<FORM ACTION=\"save_ifcs.cgi\" METHOD=POST>\n",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n<TR>",
      "<TD $tb WIDTH=100%><B>$text{'eifcs_heading'}</B></TD></TR>\n",
      "<TR><TD $cb>",
      "<INPUT TYPE=radio NAME=\"defaultroute\" VALUE=1",
      ($config->{'interfaces'} eq "%defaultroute") ? " CHECKED" : "",
      "> $text{'eifcs_defrt'}",
      "&nbsp; &nbsp;",
      "<INPUT TYPE=radio NAME=\"defaultroute\" VALUE=0",
      ($config->{'interfaces'} ne "%defaultroute") ? " CHECKED" : "",
      "> $text{'eifcs_below'}",
      "</TD></TR>\n",
      "<TR><TD><TABLE BORDER=0>",
      "<TR><TH>$text{'eifcs_name'}</TH>",
      "<TH>$text{'eifcs_mapto'}</TH>\n",
      "<TH>$text{'eifcs_name'}</TH>",
      "<TH>$text{'eifcs_mapto'}</TH></TR>\n";

@ipsecifcs=&get_ipsecifcs();

my $ifaceline = $1 if ($config->{'interfaces'} =~ /^"([\s\S]+){1}"$/);
my @ifcs=split(/ /, $ifaceline);
my %ifcs;
foreach (@ifcs) {
  /(\S+)=(\S+)/;
  $ifcs{$1}=$2;
}

for (my $i=0; $i < @ipsecifcs; $i++) {

  print "<TR>" if ($i%2==0);
  print "<TD>$ipsecifcs[$i]</TD><TD>",
        &get_iface_select($ifcs{$ipsecifcs[$i]}, "realifc$ipsecifcs[$i]"),
        "</TD>\n";
  print "</TR>" if ($i%2==1);

}
print "</TR>" if (scalar(@ipsecifcs) % 2 != 0);

print "</TABLE></TD></TR></TABLE>",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\"></FORM>\n";

print "<HR>\n";
&footer("", $text{'eifcs_return'});



### END of edit_ifcs.cgi ###.
