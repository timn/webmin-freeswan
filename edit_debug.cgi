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

&header($text{'edebug_title'}, undef, "edebug", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>";

print "<FORM ACTION=\"save_debug.cgi\" METHOD=POST>\n",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n<TR>",
      "<TD $tb WIDTH=100%><B>$text{'eifcs_heading'}</B></TD></TR>\n",
      "<TR><TD><TABLE BORDER=0>";


## Syslog Settings
print "<TR><TD COLSPAN=4><B>$text{'edebug_syslog'}</B></TD></TR>",
      "<TR><TD>$text{'edebug_syslfac'}</TD><TD>",
      "<SELECT NAME=syslfac>\n";

defined($config->{'syslog'}) || ($config->{'syslog'} = "daemon.err");
($fac, $pri) = split(/\./, $config->{'syslog'});

foreach (auth, authpriv, cron, daemon, kern, lpr, mail,
         news, syslog,  user,  uucp, local0, local1, local2, local3,
         local4, local5, local6, local7) {

  print "<OPTION VALUE=$_",
        ($_ eq $fac) ? " SELECTED" : "",
        ">$_\n";

}
print "</SELECT></TD>",
      "<TD>$text{'edebug_syslpri'}</TD><TD>",
      "<SELECT NAME=syslpri>\n";

foreach (debug,  info,  notice, warning,
         err, crit,  alert,  emerg) {

  print "<OPTION VALUE=$_",
        ($_ eq $pri) ? " SELECTED" : "",
        ">$_\n";

}
print "</SELECT></TD></TR>\n";



## Core Dump Settings
print "<TR><TD COLSPAN=4><B>$text{'edebug_coredump'}</B></TD></TR>",
      "<TR><TD COLSPAN=4>",
      "<INPUT TYPE=radio NAME=\"core\" VALUE=0",
      ($config->{'dumpdir'}) ? "" : " CHECKED",
      "> $text{'edebug_nocore'} ",
      "&nbsp; <INPUT TYPE=radio NAME=\"core\" VALUE=1",
      ($config->{'dumpdir'}) ? " CHECKED" : "",
      "> $text{'edebug_docore'} ",
      "<INPUT TYPE=text SIZE=25 NAME=coredir VALUE=\"$config->{'dumpdir'}\"> ",
      &file_chooser_button('coredir', 1),
      "</TD></TR>";


## KLIPS Debugging
$config->{'klipsdebug'} =~ s/"//g;;
my @klipsset=split(/ /, $config->{'klipsdebug'});

%klipsoptions=('tunnel'  => 'Tunnelling code',
               'xform'   => 'Transform selection and manipulation code',
               'eroute'  => 'Eroute table manipulation code',
               'spi'     => 'SA table manipulation code',
               'radij'   => 'Radij tree manipulation code',
               'esp'     => 'Encryptions transforms code',
               'ah'      => 'Authentication transforms code');

print "<TR><TD><B>$text{'edebug_klipsdebug'}</TD>",
      "<TD COLSPAN=3><INPUT TYPE=radio NAME=\"klipsmode\" VALUE=1",
      ($klipsset[0] eq 'all') ? " CHECKED" : "",
      "> $text{'edebug_all'} ",
      "<INPUT TYPE=radio NAME=\"klipsmode\" VALUE=2",
      (($klipsset[0] eq 'none') || ($klipsset[0] eq '')) ? " CHECKED" : "",
      "> $text{'edebug_none'} ",
      "<INPUT TYPE=radio NAME=\"klipsmode\" VALUE=3",
      (($klipsset[0] ne 'none') && ($klipsset[0] ne 'all') && ($klipsset[0] ne '')) ? " CHECKED" : "",
      "> $text{'edebug_listed'} ",
      "</TD></TR>",
      "<TR><TD></TD><TD COLSPAN=3><SELECT NAME=klipsdebug MULTIPLE>\n";

for (sort keys %klipsoptions) {
  print "<OPTION VALUE=\"$_\"",
        (&indexof($_, @klipsset) >= 0) ? " SELECTED" : "",
        ">$_ - $klipsoptions{$_}\n";
}
print "</SELECT></TD></TR>";



## Pluto Debugging

$config->{'plutodebug'} =~ s/"//g;;
my @plutoset=split(/ /, $config->{'plutodebug'});
%plutooptions=('raw'       => 'Show the raw bytes of messages',
               'crypt'     => 'Show the encryption and decryption of messages',
               'parsing'   => 'Show the structure of input messages',
               'emitting'  => 'Show the structure of output messages',
               'control'   => 'Show pluto\'s decision making',
               'klips'     => 'Show pluto\'s interaction with KLIPS',
               'private'   => 'Allow debugging output with private keys');

print "<TR><TD><B>$text{'edebug_plutodebug'}</TD>",
      "<TD COLSPAN=3><INPUT TYPE=radio NAME=\"plutomode\" VALUE=1",
      ($plutoset[0] eq 'all') ? " CHECKED" : "",
      "> $text{'edebug_all'} ",
      "<INPUT TYPE=radio NAME=\"plutomode\" VALUE=2",
      ($plutoset[0] eq 'none') ? " CHECKED" : "",
      "> $text{'edebug_none'} ",
      "<INPUT TYPE=radio NAME=\"plutomode\" VALUE=3",
      (($plutoset[0] ne 'none') && ($plutoset[0] ne 'all')) ? " CHECKED" : "",
      "> $text{'edebug_listed'} ",
      "</TD></TR>",
      "<TR><TD></TD><TD COLSPAN=3><SELECT NAME=plutodebug MULTIPLE>\n";

for (sort keys %plutooptions) {
  print "<OPTION VALUE=\"$_\"",
        (&indexof($_, @plutoset) >= 0) ? " SELECTED" : "",
        ">$_ - $plutooptions{$_}\n";
}
print "</SELECT></TD>",
      "</TR></TABLE></TD></TR></TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\"></FORM>\n";


print "<HR>\n";
&footer("", $text{'eifcs_return'});



### END of edit_debug.cgi ###.
