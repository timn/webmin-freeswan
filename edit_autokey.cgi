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

#    Created  : 17.09.2000


require "./freeswan-lib.pl";
&error_setup($text{'eak_err'});

$in{'conn'} || &error($text{'eak_err_mis'});

@pc=&parse_config();
my $conn=&get_section(\@pc, 'conn', $in{'conn'});
&error(&text('sconn_nof', $in{'conn'})) if (! defined($conn));


&header($text{'eak_title'}, undef, "eak", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de>Home://page</A>");
print "<BR><HR>";

print "<FORM ACTION=\"save_autokey.cgi\" METHOD=POST>\n",
      "<INPUT TYPE=hidden NAME=conn VALUE=\"$in{'conn'}\">\n",
      "<TABLE BORDER=2 CELLPADDING=2 CELLSPACING=0 $cb>\n",
      " <TR>\n",
      "  <TD $tb WIDTH=100%><B>",
      &text('eak_autokey', $in{'conn'}),
      "</B></TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100%>\n",
      "    <TR>\n",
      "     <TD><B>$text{'eak_keyex'}</B></TD>\n",
      "     <TD><SELECT NAME=keyexchange>\n",
      "<OPTION VALUE=ike",
      (! defined($conn->{'keyexchange'})
      || ( $conn->{'keyexchange'} eq 'ike')) ?
        " SELECTED" : "",
      ">IKE\n",
      "</SELECT>",
      "     </TD>\n",
      "     <TD><B>$text{'eak_perffor'}</B></TD>\n",
      "     <TD><INPUT TYPE=radio NAME=perffor VALUE=yes",
      (! defined($conn->{'pfs'}) || ($conn->{'pfs'} eq 'yes')) ?
        " CHECKED" : "",
      "> $text{'yes'} \n",
      "         <INPUT TYPE=radio NAME=perffor VALUE=no",
      ($conn->{'pfs'} eq 'no') ? " CHECKED" : "",
      "> $text{'no'} \n",
      "     </TD>\n",
      "    </TR>\n",
      "    <TR>\n",
      "     <TD><B>$text{'eak_auth'}</B></TD>\n",
      "     <TD><SELECT NAME=auth>\n",
      "<OPTION VALUE=ah",
      ($conn->{'auth'} eq 'ah') ? " SELECTED" : "",
      ">AH\n",
      "<OPTION VALUE=esp",
      (! defined($conn->{'auth'}) || ($conn->{'auth'} eq 'esp')) ?
        " SELECTED" : "",
      ">ESP\n",
      "</SELECT>",
      "     </TD>\n",
      "     <TD><B>$text{'eak_authby'}</B></TD>\n",
      "     <TD><SELECT NAME=authby>\n",
      "<OPTION VALUE=secret",
      (! defined($conn->{'authby'}) || ($conn->{'authby'} eq 'secret')) ?
        " SELECTED" : "",
      ">Shared Secret\n",
      "<OPTION VALUE=rsasig",
      ($conn->{'authby'} eq 'rsasig') ? " SELECTED" : "",
      ">RSA\n",
      "</SELECT>",
      "     </TD>\n",
      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100%>\n";

for (left, right) {

print "    <TR>\n",
      "     <TD><B>", $text{"eak_${_}id"}, "</B></TD>\n",
      "     <TD><INPUT TYPE=radio NAME=${_}def VALUE=1",
      (! defined($conn->{"${_}id"}) || ($conn->{"${_}id"} eq ${_}))
         ? " CHECKED>" : ">",
      " ", $text{"eak_${_}idauto"}, "</TD>",
      "     <TD COLSPAN=2>\n",
      " <INPUT TYPE=radio NAME=${_}def VALUE=0",
      (defined($conn->{"${_}id"}) && ($conn->{"${_}id"} ne ${_}))
        ? " CHECKED" : "",
      "> <INPUT TYPE=text NAME=${_}id VALUE=\"", $conn->{"${_}id"}, "\">",
      "</TD>\n",
      "    </TR>\n",

      "    <TR>\n",
      "     <TD><B>", $text{"eak_${_}rsa"}, "</B></TD>\n",
      "     <TD><INPUT TYPE=radio NAME=${_}rsamode VALUE=1",
      (! defined($conn->{"${_}rsasigkey"})) ? " CHECKED>" : ">",
      " $text{'eak_none'}</TD>",
      "     <TD><INPUT TYPE=radio NAME=${_}rsamode VALUE=2",
      ($conn->{"${_}rsasigkey"} eq '%dns') ? " CHECKED>" : ">",
      " $text{'eak_dns'}</TD>",
      "     <TD>\n",
      " <INPUT TYPE=radio NAME=${_}rsamode VALUE=3",
      (defined($conn->{"${_}rsasigkey"}) && ($conn->{"${_}rsasigkey"} ne '%dns'))
        ? " CHECKED" : "",
      "> <INPUT TYPE=text NAME=${_}rsa VALUE=\"",
      ($conn->{"${_}rsasigkey"} ne '%dns') ? $conn->{"${_}rsasigkey"} : '',
      "\">", $conn->{'${_}rsasigkey'},
      "</TD>\n",
      "    </TR>\n";
}


print "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      " <TR>\n",
      "  <TD>\n",
      "   <TABLE BORDER=0 WIDTH=100%>\n",
      "    <TR>\n",
      "     <TD><B>$text{'eak_keylife'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=5 NAME=keylife ",
      "VALUE=\"$conn->{'keylife'}\"></TD>\n",
      "     <TD><B>$text{'eak_rekeymargin'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=5 NAME=rekeymargin ",
      "VALUE=\"$conn->{'rekeymargin'}\"></TD>\n",
      "     <TD><B>$text{'eak_rekeyfuzz'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=5 NAME=rekeyfuzz ",
      "VALUE=\"$conn->{'rekeyfuzz'}\"></TD>\n",
      "    </TR>\n",
      "    <TR>\n",
      "     <TD><B>$text{'eak_keyingtries'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=5 NAME=keyingtries ",
      "VALUE=\"$conn->{'keyingtries'}\"></TD>\n",
      "     <TD><B>$text{'eak_ikelifetime'}</B></TD>\n",
      "     <TD><INPUT TYPE=text SIZE=5 NAME=ikelifetime ",
      " VALUE=\"$conn->{'ikelifetime'}\"></TD>\n",
      "    </TR>\n",
      "   </TABLE>\n",
      "  </TD>\n",
      " </TR>\n",
      "</TABLE>\n",
      "<INPUT TYPE=submit VALUE=\"$text{'save'}\"></FORM>\n";



print "<HR>\n";
&footer("edit_conn.cgi?conn=".&urlize($in{'conn'}),
        &text('eak_return', $in{'conn'}));



### END of edit_conn.cgi ###.
