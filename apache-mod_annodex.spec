#Module-Specific definitions
%define mod_name mod_annodex
%define mod_conf A87_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Apache module for server-side support of annodex media
Name:		apache-%{mod_name}
Version:	0.2.2
Release:	%mkrel 12
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%setup -q -n %{mod_name}-ap20-%{version}

%build

%{_sbindir}/apxs -c %{mod_name}.c `pkg-config annodex cmml --cflags --libs`

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
