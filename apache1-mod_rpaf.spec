#
# Conditional build:
%bcond_without	ipv6		# disable IPv6 support
#
%define		mod_name	rpaf
%define 	apxs		%{_sbindir}/apxs1
Summary:	Reverse proxy add forward module for Apache
Summary(pl):	Modu� Apache'a dodaj�cy przekazywanie dla odwrotnych proxy
Name:		apache1-mod_%{mod_name}
Version:	0.5
Release:	2
License:	Apache
Group:		Networking/Daemons
Source0:	http://stderr.net/apache/rpaf/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	471fb059d6223a394f319b7c8ab45c4d
Source1:	%{name}.conf
Patch0:		%{name}-ipv6.patch
URL:		http://stderr.net/apache/rpaf/
%{?with_ipv6:BuildRequires:	apache1(ipv6)-devel}
%{!?with_ipv6:BuildConflicts:	apache1(ipv6)-devel}
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1 >= 1.3.33-2
%{!?with_ipv6:Conflicts:	apache1(ipv6)}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bjoern Hansen. It will also work
with mod_proxy in Apache starting with release 1.3.25.

%description -l en
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bj�rn Hansen. It will also work
with mod_proxy in Apache starting with release 1.3.25.

%description -l pl
rpaf jest dla backendowych serwer�w Apache tym, czym
mod_proxy_add_forward jest dla frontendowych. Wykonuje dok�adnie
przeciwne operacje do mod_proxy_add_forward napisanego przez Aska
Bjoerna Hansena. B�dzie tak�e dzia�a� z mod_proxy w Apache'u pocz�wszy
od wersji 1.3.25.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%{?with_ipv6:%patch0 -p1}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/99_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES test.pl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
