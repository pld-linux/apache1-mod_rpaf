#
# Conditional build:
%bcond_without	ipv6		# disable IPv6 support
%bcond_without	tests	# do not perform "make test"

%define		mod_name	rpaf
%define 	apxs		%{_sbindir}/apxs1
Summary:	Reverse proxy add forward module for Apache
Summary(pl.UTF-8):	Moduł Apache'a dodający przekazywanie dla odwrotnych proxy
Name:		apache1-mod_%{mod_name}
Version:	0.6
Release:	2
License:	Apache
Group:		Networking/Daemons
Source0:	http://stderr.net/apache/rpaf/download/mod_rpaf-%{version}.tar.gz
# Source0-md5:	ba2b89274e1dd4c0f96f8d034fa305b1
Source1:	%{name}.conf
Patch0:		mod_rpaf_degtine.patch
Patch1:		tests.patch
URL:		http://stderr.net/apache/rpaf/
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1(EAPI)
Provides:	apache(mod_rpaf)
%if %{with ipv6}
BuildRequires:	apache1(ipv6)-devel
Requires:	apache1(ipv6)
%else
BuildConflicts:	apache1(ipv6)-devel
Conflicts:	apache1(ipv6)
%endif
%if %{with tests}
BuildRequires:	apache1-base
BuildRequires:	apache1-mod_alias
BuildRequires:	apache1-mod_cgi
BuildRequires:	apache1-mod_log_config
BuildRequires:	apache1-mod_mime
BuildRequires:	apache1-mod_rewrite
BuildRequires:	perl-libwww
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bjoern Hansen. It will also work
with mod_proxy in Apache starting with release 1.3.25.

%description -l en.UTF-8
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bjørn Hansen. It will also work
with mod_proxy in Apache starting with release 1.3.25.

%description -l pl.UTF-8
rpaf jest dla backendowych serwerów Apache tym, czym
mod_proxy_add_forward jest dla frontendowych. Wykonuje dokładnie
przeciwne operacje do mod_proxy_add_forward napisanego przez Aska
Bjoerna Hansena. Będzie także działać z mod_proxy w Apache'u począwszy
od wersji 1.3.25.

%prep
%setup -qc
mv mod_%{mod_name}-%{version}/* .
%patch0 -p1
%patch1 -p1

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%if %{with tests}
ln -sf %{_libdir}/apache1 modules
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install -p mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/99_mod_%{mod_name}.conf

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
%doc README CHANGES
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
