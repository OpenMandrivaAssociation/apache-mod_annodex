#Module-Specific definitions
%define mod_name mod_annodex
%define mod_conf A87_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module for server-side support of annodex media
Name:		apache-%{mod_name}
Version:	0.2.2
Release:	14
Group:		System/Servers
License:	Apache License
URL:		http://www.annodex.net/
Source:		http://www.annodex.net/software/mod_annodex/download/%{mod_name}-ap20-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	libannodex-devel
BuildRequires:	libcmml-devel >= 0.8
BuildRequires:	libogg-devel
BuildRequires:	pkgconfig

%description
mod_annodex provides full support for Annodex.net media. For more details about
annodex format, see http://www.annodex.net/

mod_annodex is a handler for type application/x-annodex. It provides the
following features:

        * dynamic generation of Annodex media from CMML files.

        * handling of timed query offsets, such as

          http://media.example.com/fish.anx?t=npt:01:20.8
        or
          http://media.example.com/fish.anx?id=Preparation

        * dynamic retrieval of CMML summaries, if the Accept: header
          prefers type text/x-cmml over application/x-annodex.

%prep
%autosetup -p0 -n %{mod_name}-ap20-%{version}

%build
%{_bindir}/apxs -c %{mod_name}.c `pkg-config annodex cmml --cflags --libs`

%install
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean

%files
%doc LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-12mdv2011.0
+ Revision: 678249
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-11mdv2011.0
+ Revision: 587907
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-10mdv2010.1
+ Revision: 516032
- rebuilt for apache-2.2.15

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 0.2.2-9mdv2010.1
+ Revision: 462497
- rebuild

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-8mdv2010.0
+ Revision: 406514
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-7mdv2009.1
+ Revision: 325528
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-6mdv2009.0
+ Revision: 234610
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-5mdv2009.0
+ Revision: 215520
- fix rebuild

* Thu Dec 20 2007 Olivier Blin <oblin@mandriva.com> 0.2.2-4mdv2008.1
+ Revision: 135820
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-4mdv2008.0
+ Revision: 82510
- rebuild

* Sat Aug 18 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-3mdv2008.0
+ Revision: 65615
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-2mdv2007.1
+ Revision: 140602
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-1mdv2007.1
+ Revision: 79306
- Import apache-mod_annodex

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.2.2-1mdv2007.0
- initial Mandriva package (fc5 extras import)

