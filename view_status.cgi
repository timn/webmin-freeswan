#!/usr/bin/perl
#
#    FreeS/WAN IPSEC VPN Configuration Webmin Module
#    Copyright (C) 2000-2001 by Tim Niemueller <tim@niemueller.de>
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

#    Created  : 30.12.2000

require 'freeswan-lib.pl';
@pc=&parse_config();
@conns=&get_conns(\@pc);

&header($text{'vstat_title'}, "", "intro", undef, undef, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A>".
        "<BR><A HREF=http://www.niemueller.de/>Home://page</A>");
print "<HR>\n";

print "<H3>This feature is not yet implemented</H3>";


print "<HR>";
&footer("/", $text{'vstat_return'});


### END of view_status.cgi ###.
