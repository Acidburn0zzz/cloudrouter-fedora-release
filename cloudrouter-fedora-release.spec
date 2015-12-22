%define cr_display_name CloudRouter
%define cr_name cloudrouter
%define cr_version 3
# Set this to 'Beta' or 'Release' depending on what type of release is pending.
%define release_tag Release

%define base_display_name Fedora 23
%define base_name fedora
%define base_version 23

%define project_url http://cloudrouter.org
%define bug_url https://cloudrouter.atlassian.net/secure/Dashboard.jspa

Summary:	%{cr_display_name} release files
Name:		%{cr_name}-%{base_name}-release
Version:	%{cr_version}
Release:	1
License:	AGPLv3
Group:		System Environment/Base
Source0:	GNU-AGPL-3.0.txt
Source1:	README.CloudRouter-Release-Notes

Obsoletes:	redhat-release
Obsoletes:	%{cr_name}-release
Provides:	redhat-release
Provides:	system-release
Provides:	system-release(release)
Provides:   cloudrouter-release
Requires:   cloudrouter-repo
Requires:   fedora-repos(%{base_version})
BuildArch:	noarch
Conflicts:	%{base_name}-release
Conflicts:	cloudrouter-release-%{base_name}

%description
%{cr_display_name} release files such as yum configs and various /etc/ files that
define the release.

%package notes
Summary:	Release Notes
License:	Open Publication
Group:		System Environment/Base
Provides:	system-release-notes = %{version}-%{release}
Conflicts:	%{base_name}-release-notes

%description notes
%{cr_display_name} release notes package. 

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "%{cr_display_name} release %{version} (%{release_tag})" > $RPM_BUILD_ROOT/etc/%{cr_name}-release
echo "cpe:/o:cloudrouter:cloudrouter:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/cloudrouter-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
echo >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
ln -s cloudrouter-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s cloudrouter-release $RPM_BUILD_ROOT/etc/system-release

cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME=%{cr_display_name}
VERSION="%{version} (%{release_tag})"
ID=%{cr_name}
VERSION_ID=%{version}
PRETTY_NAME="%{cr_display_name} %{version} (%{release_tag})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:cloudrouter:cloudrouter:%{version}"
HOME_URL="%{project_url}"
BUG_REPORT_URL="%{bug_url}"
EOF

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%cloudrouter		%{cr_version}
%%dist		.cr%{cr_version}
%%cr%{cr_version}		%{cr_version}
EOF

mkdir -p -m 755 $RPM_BUILD_ROOT%{_docdir}/%{cr_name}-%{base_name}-release/
install -Dpm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_docdir}/%{cr_name}-%{base_name}-release/
install -Dpm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_docdir}/%{cr_name}-%{base_name}-release/

%clean
rm -rf $RPM_BUILD_ROOT

%post
# fix yum.conf
sed -i s-"^bugtracker_url=.*$"-"bugtracker_url=%{bug_url}"- /etc/yum.conf
sed -i s/"^distroverpkg=.*$"/"distroverpkg=%{name}"/ /etc/yum.conf

%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{cr_name}-%{base_name}-release/%{SOURCE0}
%config %attr(0644,root,root) /etc/os-release
%config %attr(0644,root,root) /etc/%{cr_name}-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%defattr(0644,root,root,0755)

%files notes
%defattr(-,root,root,-)
%doc %{_docdir}/%{cr_name}-%{base_name}-release/%{SOURCE1}

%changelog
* Tue Dec 15 2015 John Siegrist <john@complects.com> - 3-1
- Rebase to F23 and bump version to CRv3.

* Thu Aug 27 2015 John Siegrist <john@complects.com> - 2-3
- Added support for virtual package "cloudrouter-repo".

* Fri Aug 14 2015 John Siegrist <john@complects.com> - 2-2
- Fixed GPG key verification for RPMs downloaded from the CloudRouter repository.

* Mon Aug 10 2015 John Siegrist <john@complects.com> - 2-1
- Initial commit of the Fedora-specific CloudRouter-release project after splitting it into separate ones for Fedora and CentOS.
