#!/usr/bin/perl
#
#    FreeS/WAN IPSEC VPN Configuration Webmin Module
#    Copyright (C) 1999-2000 by Tim Niemueller <tim@niemueller.de>
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

#    Created  : 25.09.2000


require "./freeswan-lib.pl";
my @pc=&parse_config();
my @conns=&get_conns(\@pc);
my $config=&get_section(\@pc, 'config', 'setup');

&header($text{'estart_title'}, undef, "estart", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>";

print "<FORM ACTION=\"save_start.cgi\" METHOD=POST>\n",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n<TR>",
      "<TD $tb WIDTH=100%><B>$text{'estart_load'}</B></TD></TR>\n",
      "<TR><TD $cb>",
      "<INPUT TYPE=radio NAME=\"loadmode\" VALUE=1",
      (! defined($config->{'plutoload'})) ? " CHECKED" : "",
      "> $text{'estart_none'}",
      "&nbsp; &nbsp;",
      "<INPUT TYPE=radio NAME=\"loadmode\" VALUE=2",
      ($config->{'plutoload'} eq "%search") ? " CHECKED" : "",
      "> $text{'estart_search'}",
      "&nbsp; &nbsp;",
      "<INPUT TYPE=radio NAME=\"loadmode\" VALUE=3",
      ((defined($config->{'plutoload'})) && ($config->{'plutoload'} ne "%search")) ? " CHECKED" : "",
      "> $text{'estart_below'}",
      "</TD></TR>\n",
      "<TR><TD><SELECT NAME=load MULTIPLE SIZE=4>\n";

my $loadline = $1 if ($config->{'plutoload'} =~ /^"([\s\S]+){1}"$/);
my @loaded=split(/ /, $loadline);

for (my $i=0; $i < @conns; $i++) {

  print "<OPTION",
        (&indexof($conns[$i], @loaded) >= 0) ? " SELECTED>" : ">",
        "$conns[$i]\n";

}

print "</SELECT></TD></TR>\n",
      "</TABLE></TD></TR></TABLE><BR>",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n<TR>",
      "<TD $tb WIDTH=100%><B>$text{'estart_start'}</B></TD></TR>\n",
      "<TR><TD $cb>",
      "<INPUT TYPE=radio NAME=\"startmode\" VALUE=1",
      (! defined($config->{'plutostart'})) ? " CHECKED" : "",
      "> $text{'estart_none'}",
      "&nbsp; &nbsp;",
      "<INPUT TYPE=radio NAME=\"startmode\" VALUE=2",
      ($config->{'plutostart'} eq "%search") ? " CHECKED" : "",
      "> $text{'estart_search'}",
      "&nbsp; &nbsp;",
      "<INPUT TYPE=radio NAME=\"startmode\" VALUE=3",
      ((defined($config->{'plutostart'})) && ($config->{'plutostart'} ne "%search")) ? " CHECKED" : "",
      "> $text{'estart_below'}",
      "</TD></TR>\n",
      "<TR><TD><SELECT NAME=start MULTIPLE SIZE=4>\n";


my $startline = $1 if ($config->{'plutostart'} =~ /^"([\s\S]+){1}"$/);
my @started=split(/ /, $startline);

for (my $i=0; $i < @conns; $i++) {

  print "<OPTION",
        (&indexof($conns[$i], @started) >= 0) ? " SELECTED>" : ">",
        "$conns[$i]\n";

}
print "</SELECT></TD></TR>\n",
      "</TABLE></TD></TR></TABLE>",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\"></FORM>\n";

print "<HR>\n";
&footer("", $text{'estart_return'});



### END of edit_start.cgi ###.
