Name:           openstack-xen-networking
Version:        2012.1
Release:        1
Summary:        Files for XenAPI network hosst/vif rules/ovs support.
License:        ASL 2.0
Group:          Applications/Utilities
Source0:        openstack-xen-networking.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       iptables ebtables arptables_jf python-simplejson

%define debug_package %{nil}

%description
This package contains files that are required for Host vif rules and ovs additions for OpenStack.

%prep
%setup -q -n openstack-xen-networking

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/init.d
mkdir -p $RPM_BUILD_ROOT/etc/xensource/scripts
cp -r etc/init.d/host-rules $RPM_BUILD_ROOT/etc/init.d/
cp -r etc/xensource/scripts/vif_rules.py $RPM_BUILD_ROOT/etc/xensource/scripts/
cp -r etc/xensource/scripts/vif_6.0.patch $RPM_BUILD_ROOT/etc/xensource/scripts/
cp -r etc/xensource/scripts/novalib.py $RPM_BUILD_ROOT/etc/xensource/scripts/

%post
cd /etc/xensource/scripts
patch -r - -N < vif_6.0.patch
chkconfig host-rules on
/etc/init.d/host-rules start

%preun
/etc/init.d/host-rules stop
chkconfig host-rules off
cd /etc/xensource/scripts
patch -r - -R < vif_6.0.patch

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/etc/init.d/host-rules
/etc/xensource/scripts/vif_rules.py
/etc/xensource/scripts/vif_6.0.patch
/etc/xensource/scripts/novalib.py
