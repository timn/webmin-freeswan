#!/usr/bin/perl
#
#    FreeS/WAN IPSEC VPN Configuration Webmin Module
#    Copyright (C) 2000 by Tim Niemueller <tim@niemueller.de>
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

#    Created on Sep 14th 2000, 8:46 EST

require 'freeswan-lib.pl';
@pc=&parse_config();
@conns=&get_conns(\@pc);

&header($text{'index_title'}, "", "intro", 1, 1, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de/>Home://page</A>");
print "<HR>\n";


my @images = ("images/icon.ifaces.gif", "images/icon.debug.gif",
              "images/icon.info.gif", "images/icon.pluto.gif",
              "images/icon.default.gif", "images/icon.status.gif",
              "images/icon.onstart.gif", "images/icon.keys.gif");
my @texts  = ($text{'index_ifaces'}, $text{'index_debug'},
              $text{'index_info'}, $text{'index_pluto'},
              $text{'index_defaultc'}, $text{'index_status'},
              $text{'index_loadconn'}, $text{'index_keys'});
my @links  = ("edit_ifcs.cgi", "edit_debug.cgi",
              "view_info.cgi", "edit_pluto.cgi",
              "edit_conn.cgi?conn=".&urlize("%default"), "view_status.cgi",
              "edit_start.cgi", "list_keys.cgi");

&icons_table(\@links, \@texts, \@images, 4);
print "<HR>",
      "<H3>$text{'index_conns'}</H3>\n";


my @connimgs=();
my @conntexts=();
my @connlinks=();

foreach (@conns) {
  push(@connimgs, "images/icon.conn.gif");
  push(@conntexts, $_);
  push(@connlinks, "edit_conn.cgi?conn=".&urlize($_));
}


if (scalar(@conns)) {
  &icons_table(\@connlinks, \@conntexts, \@connimgs, 4);
} else {
  print "<B>$text{'index_noconn'}</B><BR><BR>";
}

#foreach $l (@pc) {
# print "$l->{'type'} $l->{'name'}<UL>\n";

# for (keys %{$l}) {
#   print "$_: $l->{$_}<BR>\n";
# }

#print "</UL>\n";
#}

print "<TABLE BORDER=0 WIDTH=100%><TR><TD ALIGN=right>",
      "<FONT FACE=\"Arial,helvetica\" COLOR=\"#505050\">[ $version ] </FONT>",
      "</TD></TR></TABLE><HR>";


&footer("/", $text{'index'});


### END of index.cgi ###.
