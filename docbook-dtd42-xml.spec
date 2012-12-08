%define dtdver 4.2
%define mltyp xml

Name:    docbook-dtd42-xml
Version: 1.0
Release: 15
Group:   Publishing
Summary: XML document type definition for DocBook %{dtdver}
License: Artistic
URL:     http://www.oasis-open.org/docbook/
Provides: docbook-dtd-%{mltyp}
Requires(post): sgml-common coreutils
Requires(postun): sgml-common coreutils

# Zip file downloadable at http://www.oasis-open.org/docbook/%{mltyp}/%{dtdver}
Source0:   docbook-xml-4.2.tar.bz2 
BuildArch: noarch  


%define sgmlbase %{_datadir}/sgml

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.

%prep
%setup -n docbook-xml-4.2 -q

%build

%install
DESTDIR=%{buildroot}/%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
mkdir -p $DESTDIR
cp -r ent/ $DESTDIR
install -m644 docbook.cat $DESTDIR/catalog
install -m644 catalog.xml $DESTDIR
install -m644 *.dtd $DESTDIR
install -m644 *.mod $DESTDIR
mkdir -p %{buildroot}/%{_sysconfdir}/sgml
touch %{buildroot}/%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
touch %{buildroot}/%{_sysconfdir}/sgml/catalog

%post
##
## SGML catalog
##
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
if [ -e %{sgmlbase}/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/openjade/catalog
fi

if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/dsssl-stylesheets/catalog
fi
# Symlinks
[ ! -e %{_sysconfdir}/sgml/%{mltyp}-docbook.cat ] && \
	ln -s %{mltyp}-docbook-%{dtdver}.cat %{_sysconfdir}/sgml/%{mltyp}-docbook.cat

##
## XML catalog
##

CATALOG=%{sgmlbase}/docbook/xmlcatalog

%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML V4.2//EN" \
	"file:///usr/share/sgml/docbook/xml-dtd-4.2/catalog.xml" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://www.oasis-open.org/docbook/xml/4.2" \
	"xml-dtd-4.2" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://www.oasis-open.org/docbook/xml/4.2" \
	"xml-dtd-4.2" $CATALOG

%postun
##
## SGML catalog
##
# Do not remove if upgrade
if [ "$1" = "0" ]; then
  if [ -x %{_bindir}/xmlcatalog ]; then 
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog
  fi
 # Symlinks
 [ -e %{_sysconfdir}/sgml/%{mltyp}-docbook.cat ] && \
	 rm -f %{_sysconfdir}/sgml/%{mltyp}-docbook.cat

 if [ -x %{_bindir}/xmlcatalog ]; then

  # The following lines are for the case in which the style sheets
  # were not uninstalled because there is still another DTD
  if [ -e %{sgmlbase}/openjade/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/openjade/catalog
  fi

  if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/docbook/dsssl-stylesheets/catalog
  fi
 fi

##
## XML catalog
##

  CATALOG=%{sgmlbase}/docbook/xmlcatalog

  if [ -w $CATALOG -a -x %{_bindir}/xmlcatalog ]; then
   %{_bindir}/xmlcatalog --noout --del \
  	   "-//OASIS//DTD DocBook XML V4.2//EN" $CATALOG
   %{_bindir}/xmlcatalog --noout --del \
	   "xml-dtd-4.2" $CATALOG
  fi
fi

%files
%doc README ChangeLog
%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
%ghost %config(noreplace) %{_sysconfdir}/sgml/catalog


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-13mdv2011.0
+ Revision: 663828
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-12mdv2011.0
+ Revision: 604803
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-11mdv2010.1
+ Revision: 520688
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-10mdv2010.0
+ Revision: 413366
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.0-9mdv2009.0
+ Revision: 220672
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.0-8mdv2008.1
+ Revision: 149190
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1.0-7mdv2008.0
+ Revision: 70194
- convert prereq

* Tue Jun 26 2007 Adam Williamson <awilliamson@mandriva.org> 1.0-6mdv2008.0
+ Revision: 44236
- rearrange spec, update requires, rebuild for 2008
- Import docbook-dtd42-xml


 
* Mon Jun  5 2006 Camille Begnis <camille@mandriva.com> 1.0-5mdv2007.0
- rebuild

* Mon May 16 2005 Camille Begnis <camille@mandrakesoft.com> 1.0-5mdk
- rebuild
- fix license to please rpmlint

* Thu Apr 22 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-4mdk
- Fix uninstall when xmlcatalog is no longer present

* Mon Jul 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-3mdk
- Add some ghost/config files to package
- Fix buggy postun scripts

* Fri Jul 18 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 1.0-2mdk
- fix uninstall script : only unregister from existing catalog

* Mon Dec  2 2002  <camille@ke.mandrakesoft.com> 1.0-1mdk
- First specs for MDK
