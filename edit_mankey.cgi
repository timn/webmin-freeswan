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

#    Created  : 17.09.2000


require "./freeswan-lib.pl";
&error_setup($text{'emk_err'});

$in{'conn'} || &error($text{'emk_err_mis'});

@pc=&parse_config();
my $conn=&get_section(\@pc, 'conn', $in{'conn'});
&error(&text('sconn_nof', $in{'conn'})) if (! defined($conn));


&header($text{'emk_title'}, undef, "emk", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>";

print "<FORM ACTION=\"save_mankey.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=conn VALUE=\"$in{'conn'}\">\n",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      &text('emk_mankey', $in{'conn'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100%>\n",
      "    <TR>\n",
      "     <TD><B>$text{'emk_spi'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=5 NAME=spi VALUE=\"$conn->{'spi'}\"></TD>\n",
      "     <TD><B>$text{'emk_spibase'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=5 NAME=spibase VALUE=\"$conn->{'spibase'}\"></TD>\n",
      "     </TD>\n",
      "    </TR>\n",
      "    <TR>\n",
      "     <TD><B>$text{'emk_esp'}</B></TD>\n",

      "     <TD><SELECT NAME=esp>\n",
      "<OPTION VALUE=\"\"",
      (! defined($conn->{'esp'})) ? " SELECTED>" : ">",
      "$text{'emk_espnone'}\n",
      "<OPTION VALUE=\"3des\"",
      ($conn->{'esp'} eq '3des') ? " SELECTED>" : ">",
      "3DES\n",
      "<OPTION VALUE=\"3des-md5-96\"",
      ($conn->{'esp'} eq '3des-md5-96') ? " SELECTED>" : ">",
      "3DES-MD5-96\n",
      "<OPTION VALUE=\"3des-sha1-96\"",
      ($conn->{'esp'} eq '3des-sha1-96') ? " SELECTED>" : ">",
      "3DES-SHA1-96\n",
      "<OPTION VALUE=\"null-md5-96\"",
      ($conn->{'esp'} eq 'null-md5-96') ? " SELECTED>" : ">",
      "Null-MD5-96\n",
      "<OPTION VALUE=\"null-sha1-96\"",
      ($conn->{'esp'} eq 'null-sha1-96') ? " SELECTED>" : ">",
      "Null-SHA1-96\n",
      "</SELECT>",
      "     </TD>\n",
      "     <TD><B>$text{'emk_ah'}</B></TD>\n",
      "     <TD><SELECT NAME=ah>\n",
      "<OPTION VALUE=\"\"",
      (! defined($conn->{'ah'})) ? " SELECTED>" : ">",
      "$text{'emk_ahnone'}\n",
      "<OPTION VALUE=\"hmac-md5-96\"",
      ($conn->{'ah'} eq 'hmac-md5-96') ? " SELECTED>" : ">",
      "HMAC-MD5-96\n",
      "<OPTION VALUE=\"hmac-sha1-96\"",
      ($conn->{'ah'} eq 'hmac-sha1-96') ? " SELECTED>" : ">",
      "HMAC-SHA1-96\n",

      "</SELECT>",
      "     </TD>\n",
      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100%>\n",
      "    <TR>\n",
      "     <TD><B>$text{'emk_espenckey'}</B></TD>\n",
      "     <TD><INPUT TYPE=radio NAME=useespenckey VALUE=1",
      (! defined($conn->{'espenckey'})) ? " CHECKED> " : "> ",
      "$text{'emk_ipssec'} <INPUT TYPE=radio NAME=useespenckey VALUE=2>",
      "$text{'emk_auto'} <INPUT TYPE=radio NAME=useespenckey VALUE=3",
      (defined($conn->{'espenckey'})) ? " CHECKED> " : "> ",
      "<INPUT TYPE=text SIZE=40 NAME=espenckey VALUE=\"$conn->{'espenckey'}\"></TD>\n",
      "    </TR>\n",

      "    <TR>\n",
      "     <TD><B>$text{'emk_espauthkey'}</B></TD>\n",
      "     <TD><INPUT TYPE=radio NAME=useespauthkey VALUE=1",
      (! defined($conn->{'espauthkey'})) ? " CHECKED> " : "> ",
      "$text{'emk_ipssec'} <INPUT TYPE=radio NAME=useespauthkey VALUE=2>",
      "$text{'emk_auto'} <INPUT TYPE=radio NAME=useespauthkey VALUE=3",
      (defined($conn->{'espauthkey'})) ? " CHECKED> " : "> ",
      "<INPUT TYPE=text SIZE=40 NAME=espauthkey VALUE=\"$conn->{'espauthkey'}\"></TD>\n",
      "    </TR>\n",


      "    <TR>\n",
      "     <TD><B>$text{'emk_ahauthkey'}</B></TD>\n",
      "     <TD><INPUT TYPE=radio NAME=useahauthkey VALUE=1",
      (! defined($conn->{'ahauthkey'})) ? " CHECKED> " : "> ",
      "$text{'emk_ipssec'} <INPUT TYPE=radio NAME=useahauthkey VALUE=2>",
      "$text{'emk_auto'} <INPUT TYPE=radio NAME=useahauthkey VALUE=3",
      (defined($conn->{'ahauthkey'})) ? " CHECKED> " : "> ",
      "<INPUT TYPE=text SIZE=40 NAME=ahauthkey VALUE=\"$conn->{'ahauthkey'}\"></TD>\n",
      "    </TR>\n",

      "    <TR>\n",
      "     <TD><B>$text{'emk_ahrwin'}</B></TD>\n",
      "     <TD><SELECT NAME=ahrwin>\n",
      "<OPTION",
      ((! defined($conn->{'ahreplay_window'})) || ($conn->{'ahreplay_window'} == 0)) ? " SELECTED" : "",
      ">0\n";

for (my $i=1; $i<65; $i++) {
  print "<OPTION",
        ($conn->{'ahreplay_window'} == $i) ? " SELECTED" : "",
        ">$i\n";
}
print "</SELECT></TD>\n",
      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=4>\n",
      "    <TR>\n";


for (left, right) {

print "     <TD WIDTH=50%>\n",
      "      <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=0 WIDTH=100%>\n",
      "       <TR>\n",
      "        <TD>\n",
      "         <TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb WIDTH=100%>\n",
      "          <TR>\n",
      "           <TD $tb WIDTH=100%><B>", $text{"emk_$_"},
      "</B></TD>\n",
      "          </TR>\n",
      "          <TR>\n",
      "           <TD>\n",
      "            <TABLE BORDER=0 WIDTH=100% CELLPADDING=0 CELLSPACING=0>\n",
      "             <TR>\n",
      "              <TD><B>$text{'emk_espspi'}</B></TD>\n",
      "             <TD><INPUT TYPE=text SIZE=5 MAXLENGTH=5 NAME=${_}espspi",
      " VALUE=\"", $conn->{"${_}espspi"}, "\"></TD>\n",
      "             </TR>\n",
      "             <TR>\n",
      "              <TD><B>$text{'emk_ahspi'}</B></TD>\n",
      "              <TD><INPUT TYPE=text SIZE=5 MAXLENGTH=5 NAME=${_}ahspi",
      " VALUE=\"", $conn->{"${_}ahspi"}, "\"></TD>\n",
      "             </TR>\n",
      "             <TR>\n",
      "              <TD COLSPAN=2><HR SIZE=1 NOSHADE></TD>\n",
      "             </TR>",



      "             <TR>\n",
      "              <TD><B>$text{'emk_espenckey'}</B></TD>\n",
      "              <TD><INPUT TYPE=radio NAME=use${_}espenckey VALUE=1",
      (! defined($conn->{"${_}espenckey"})) ? " CHECKED> " : "> ",
      "$text{'emk_none'} <INPUT TYPE=radio NAME=use${_}espenckey VALUE=2>",
      "$text{'emk_auto'}<BR><INPUT TYPE=radio NAME=use${_}espenckey VALUE=3",
      (defined($conn->{"${_}espenckey"})) ? " CHECKED> " : "> ",
      "<INPUT TYPE=text SIZE=20 NAME=${_}espenckey VALUE=\"",
      $conn->{"${_}espenckey"}, "\"></TD>\n",
      "             </TR>\n",

      "             <TR>\n",
      "              <TD COLSPAN=2><HR SIZE=1 NOSHADE></TD>\n",
      "             </TR>",

      "             <TR>\n",
      "              <TD><B>$text{'emk_espauthkey'}</B></TD>\n",
      "              <TD><INPUT TYPE=radio NAME=use${_}espauthkey VALUE=1",
      (! defined($conn->{"${_}espauthkey"})) ? " CHECKED> " : "> ",
      "$text{'emk_none'} <INPUT TYPE=radio NAME=use${_}espauthkey VALUE=2>",
      "$text{'emk_auto'}<BR><INPUT TYPE=radio NAME=use${_}espauthkey VALUE=3",
      (defined($conn->{"${_}espauthkey"})) ? " CHECKED> " : "> ",
      "<INPUT TYPE=text SIZE=20 NAME=${_}espauthkey VALUE=\"",
      $conn->{"${_}espauthkey"}, "\"></TD>\n",
      "             </TR>\n",

      "             <TR>\n",
      "              <TD COLSPAN=2><HR SIZE=1 NOSHADE></TD>\n",
      "             </TR>",

      "             <TR>\n",
      "              <TD><B>$text{'emk_ahauthkey'}</B></TD>\n",
      "              <TD><INPUT TYPE=radio NAME=use${_}ahauthkey VALUE=1",
      (! defined($conn->{"${_}ahauthkey"})) ? " CHECKED> " : "> ",
      "$text{'emk_none'} <INPUT TYPE=radio NAME=use${_}ahauthkey VALUE=2>",
      "$text{'emk_auto'}<BR><INPUT TYPE=radio NAME=use${_}ahauthkey VALUE=3",
      (defined($conn->{"${_}ahauthkey"})) ? " CHECKED> " : "> ",
      "<INPUT TYPE=text SIZE=20 NAME=${_}ahauthkey VALUE=\"",
      $conn->{"${_}ahauthkey"}, "\"></TD>\n",
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
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\"></FORM>\n";



print "<HR>\n";
&footer("edit_conn.cgi?conn=".&urlize($in{'conn'}),
        &text('eak_return', $in{'conn'}));



### END of edit_mankey.cgi ###.
