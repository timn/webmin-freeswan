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
my $config;
foreach (@pc) {
  if (($_->{'sectiontype'} eq 'config') && ($_->{'name'} eq 'setup')) {
    $config=$_;
    last;
  }
}

&header($text{'epluto_title'}, undef, "epluto", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>";

print "<FORM ACTION=\"save_pluto.cgi\" METHOD=POST>\n",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n<TR>",
      "<TD $tb WIDTH=100%><B>$text{'epluto_heading'}</B></TD></TR>\n",
      "<TR><TD><TABLE BORDER=0>",
      "<TR><TD><B>$text{'epluto_run'}</B></TD><TD>",
      "<INPUT TYPE=radio NAME=\"run\" VALUE=yes",
      (! $config->{'pluto'} || ($config->{'pluto'} eq 'yes')) ? " CHECKED" : "",
      "> $text{'yes'} ",
      "&nbsp; <INPUT TYPE=radio NAME=\"run\" VALUE=no",
      ($config->{'pluto'} eq "no") ? " CHECKED" : "",
      "> $text{'no'} </TD></TR>",

      "<TR><TD><B>$text{'epluto_wait'}</B></TD><TD>",
      "<INPUT TYPE=radio NAME=\"wait\" VALUE=yes",
      (! $config->{'plutowait'} || ($config->{'plutowait'} eq 'yes')) ?
         " CHECKED" : "",
      "> $text{'yes'} ",
      "&nbsp; <INPUT TYPE=radio NAME=\"wait\" VALUE=no",
      ($config->{'plutowait'} eq "no") ? " CHECKED" : "",
      "> $text{'no'} </TD></TR>",

      "<TR><TD><B>$text{'epluto_bg'}</B></TD><TD>",
      "<INPUT TYPE=radio NAME=\"bg\" VALUE=yes",
      ($config->{'plutobackgroundload'} eq 'yes') ? " CHECKED" : "",
      "> $text{'yes'} ",
      "&nbsp; <INPUT TYPE=radio NAME=\"bg\" VALUE=no",
      (! $config->{'plutobackgroundload'} ||
      ($config->{'plutobackgroundwait'} eq "no")) ? " CHECKED" : "",
      "> $text{'no'} </TD></TR>",

      "<TR><TD><B>$text{'epluto_pre'}</B></TD>",
      "<TD><INPUT TYPE=text NAME=pre VALUE=\"$config->{'prepluto'}\"> ",
      &file_chooser_button('pre'),
      "</TD></TR>\n",

      "<TR><TD><B>$text{'epluto_post'}</B></TD>",
      "<TD><INPUT TYPE=text NAME=post VALUE=\"$config->{'postpluto'}\"> ",
      &file_chooser_button('post'),
      "</TD></TR>\n";


print "</TABLE></TD></TR></TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\"></FORM>\n";


print "<HR>\n";
&footer("", $text{'epluto_return'});



### END of edit_pluto.cgi ###.
