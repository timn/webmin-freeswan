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

#    Created  : 16.09.2000


require "./freeswan-lib.pl";
&error_setup($text{'econn_err'});

$in{'conn'} || &error($text{'econn_err_mis'});

@pc=&parse_config();
my $conn=&get_section(\@pc, 'conn', $in{'conn'});
&error(&text('sconn_nof', $in{'conn'})) if (! defined($conn));


&header($text{'econn_title'}, undef, "econn", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>";

print "<FORM ACTION=\"save_conn.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=conn VALUE=\"$in{'conn'}\">",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>$text{'econn_general'} $in{'conn'}</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",

      "    <TR>\n",
      "     <TD COLSPAN=2>\n",
      "      <TABLE BORDER=0>\n",

      "       <TR>\n",
      "        <TD><B>$text{'econn_type'}</B></TD>\n",
      "        <TD><SELECT NAME=type>\n",
      "<OPTION VALUE=tunnel",
      (! defined($conn->{'type'}) ||
        ($conn->{'type'} eq 'tunnel')) ? " SELECTED" : "",
      ">$text{'econn_type_tunnel'}\n",
      "<OPTION VALUE=transport",
      ($conn->{'type'} eq 'transport') ? " SELECTED" : "",
      ">$text{'econn_type_transport'}\n",
      "<OPTION VALUE=passthrough",
      ($conn->{'type'} eq 'passthrough') ? " SELECTED" : "",
      ">$text{'econn_type_passthrough'}\n",
      "</SELECT></TD>",

      "        <TD><B>$text{'econn_auto'}</B></TD>\n",
      "        <TD><SELECT NAME=auto>\n",
      "<OPTION VALUE=ignore",
      (! defined($conn->{'auto'}) ||
        ($conn->{'auto'} eq 'ignore')) ? " SELECTED" : "",
      ">$text{'econn_auto_ignore'}\n",
      "<OPTION VALUE=add",
      ($conn->{'auto'} eq 'add') ? " SELECTED" : "",
      ">$text{'econn_auto_add'}\n",
      "<OPTION VALUE=start",
      ($conn->{'auto'} eq 'start') ? " SELECTED" : "",
      ">$text{'econn_auto_start'}\n",
      "</SELECT></TD>\n",
      "        <TD><B>$text{'econn_compress'}</B></TD>\n",
      "        <TD><INPUT TYPE=radio NAME=compress VALUE=yes",
      ($conn->{"compress"} eq "yes") ? " CHECKED" : "",
      "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=compress VALUE=no",
      (! defined($conn->{"compress"}) ||
        ($conn->{"${_}firewall"} eq "no")) ? " CHECKED" : "",
      "> $text{'no'}</TD>\n",
      "       </TR>\n",
      "      </TABLE>\n",
      "     </TD>\n",
      "    </TR>\n",

      "    <TR>\n";

for (left, right) {

print "     <TD WIDTH=50%>\n",
      "      <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=0 WIDTH=100%>\n",
      "       <TR>\n",
      "        <TD>\n",
      "         <TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      "          <TR>\n",
      "           <TD $tb WIDTH=100%><B>", $text{"econn_$_"}, "</B></TD>\n",
      "          </TR>\n",
      "          <TR>\n",
      "           <TD>\n",
      "            <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=0>\n",
      "             <TR>\n",
      "              <TD><B>$text{'econn_ip'}</B></TD>\n",
      "              <TD><INPUT TYPE=text SIZE=15 MAXLENGTH=15 NAME=$_",
      " VALUE=\"", $conn->{"$_"}, "\"></TD>\n",
      "             </TR>\n",
      "             <TR>\n",
      "              <TD><B>$text{'econn_sub'}</B></TD>\n",
      "              <TD><INPUT TYPE=text SIZE=18 MAXLENGTH=18 NAME=sub$_",
      " VALUE=\"", $conn->{"${_}subnet"}, "\"></TD>\n",
      "             </TR>\n",
      "             <TR>\n",
      "              <TD><B>$text{'econn_gate'}</B></TD>\n",
      "              <TD><INPUT TYPE=text SIZE=15 MAXLENGTH=15 NAME=gate$_",
      " VALUE=\"", $conn->{"${_}nexthop"}, "\"></TD>\n",
      "             </TR>\n",
      "             <TR>\n",
      "              <TD><B>$text{'econn_updown'}</B></TD>\n",
      "              <TD><INPUT TYPE=text SIZE=15 NAME=updown$_",
      " VALUE=\"", $conn->{"${_}updown"}, "\"> ",
      &file_chooser_button("updown$_"),
      "</TD>\n",
      "             </TR>\n",
      "             <TR>\n",
      "              <TD><B>$text{'econn_fw'}</B></TD>\n",
      "              <TD><INPUT TYPE=radio NAME=fw$_ VALUE=yes",
      ($conn->{"${_}firewall"} eq "yes") ? " CHECKED" : "",
      "> $text{'yes'} ",
      "<INPUT TYPE=radio NAME=fw$_ VALUE=no",
      (! defined($conn->{"${_}firewall"}) ||
        ($conn->{"${_}firewall"} eq "no")) ? " CHECKED" : "",
      "> $text{'no'}</TD>\n",
     

      "             </TR>\n",
      "            </TABLE>\n",
      "           </TD>\n",
      "          </TR>\n",
      "         </TABLE>\n",
      "        </TD>\n",
      "       </TR>\n",
      "      </TABLE>\n",
      "     </TD>\n",
}

print "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100%>\n",
      "    <TR>\n",
      "     <TD WIDTH=50% ALIGN=center><A HREF=\"edit_autokey.cgi?conn=",
      &urlize($in{'conn'}),
      "\">$text{'econn_eak'}</A></TD>",
      "     <TD WIDTH=50% ALIGN=center><A HREF=\"edit_mankey.cgi?conn=",
      &urlize($in{'conn'}),
      "\">$text{'econn_emk'}</A></TD>",
      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\"></FORM>\n";



print "<HR>\n";
&footer("", $text{'econn_return'});



### END of edit_conn.cgi ###.
