%define tarball xf86-video-nouveau
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
%define nouveau_version 0.0.16

# Tarfile created using git
# git clone git://git.freedesktop.org/git/nouveau/xf86-video-nouveau
# git-archive --format=tar --prefix=xf86-video-nouveau-0.0.10/ %{git_version} | bzip2 > xf86-video-nouveau-0.0.10-%{gitdate}.tar.bz2

%define gitdate 20100423
%define git_version 13c1043

%define snapshot %{gitdate}git%{git_version}

%define tarfile %{tarball}-%{nouveau_version}-%{snapshot}.tar.bz2

Summary:   Xorg X11 nouveau video driver for NVIDIA graphics chipsets
Name:      xorg-x11-drv-nouveau
# need to set an epoch to get version number in sync with upstream
Epoch:     1
Version:   %{nouveau_version}
Release:   8.%{snapshot}%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Fedora specific snapshot no upstream release
Source0:   %{tarfile}

ExcludeArch: s390 s390x

BuildRequires: libtool automake autoconf
BuildRequires: xorg-x11-server-devel > 1.6.99-36
BuildRequires: libdrm-devel >= 2.4.19-3
BuildRequires: mesa-libGL-devel
BuildRequires: libudev-devel

Requires:  hwdata
Requires:  xorg-x11-server-Xorg > 1.6.99-36
Requires:  libdrm >= 2.4.19-3
Requires:  kernel-drm-nouveau = 16

Patch0: nouveau-nva0-corruption-fix.patch
Patch1: nouveau-bgnr.patch
Patch2: nouveau-exa-no-pa_fa.patch
Patch3: nouveau-zfill-fallback.patch
Patch4: nouveau-server-regen.patch

%description 
X.Org X11 nouveau video driver.

%prep
%setup -q -n %{tarball}-%{version}

%patch0 -p1 -b .tile7000
%patch1 -p1 -b .bgnr
%patch2 -p1 -b .no_wfb
%patch3 -p1 -b .zfill
%patch4 -p1 -b .regen

%build
autoreconf -v --install
%configure --disable-static --with-kms=yes

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/nouveau_drv.so
%{_mandir}/man4/nouveau.4*

%changelog
* Fri Jun 11 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-8.20100423git13c1043
- Fix server regeneration (rh#601790)

* Wed Jun 09 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-7.20100423git13c1043
- Disallow direct CPU access to pixmaps to avoid using (slow) wfb (rh#595405)

* Tue May 11 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-6.20100423git13c1043
- Fix server crashes with no outputs connected
- Fix pixmap corruption on certain chipsets

* Tue Apr 13 2010 Dennis Gregorovic <dgregor@redhat.com> - 1:0.0.16-5.20100318gite2146d3.1
- Bump for rebuild

* Thu Mar 25 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-5.20100318gite2146d3
- bump libdrm requires

* Thu Mar 25 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.16-4.20100318gite2146d3
- Sync up with F13/upstream, brings support for kernel ABI break

* Mon Jan 25 2010 Ben Skeggs <bskeggs@redhat.com> 0.0.15-19.20091105gite1c2efd
- Sync up fixes from current F12 package
- nouveau-kms-noaccel-fixes.patch: fix crash on fb resize when using
  shadowfb (rh#538238)
- nouveau-nv04_nodcb.patch: assume nv04 doesn't have a DCB table (rh#555202)
- nouveau-randr-fixes.patch: fix fb resize/rotate on <nv50 (rh#532978)
- nouveau-libdrm-compat.patch: fix build against libdrm 2.4.17

* Thu Nov 05 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-17.20091105gite1c2efd
- handle reloc failures more gracefully (rh#531058)
- fix for rh#532322

* Mon Nov 02 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-16.20091030git5587f40
- force all pixmaps into system memory initally on low memory cards

* Tue Oct 27 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-15.20091022git718a41b
- misc fixes, initial NVA8 support

* Thu Oct 09 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-14.20091008git3f020b0
- update from upstream, fixes various issues, especially with recent xservers

* Tue Sep 29 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-13.20090929gitdd8339f
- fix driver to work again with recent EXA changes

* Fri Sep 25 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-12.20090924gitde0b095
- G80: small performance fix

* Mon Sep 21 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-11.20090921gitdf95ebd
- fix an accel pitch issue seen in rh#523281

* Mon Sep 14 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-10.20090914git1b72020
- wait for fbcon copy to complete before switching mode (rh#522688)

* Thu Sep 10 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-9.20090910git806eaf6
- fix a hang/crash issue that could occur during a modeset
- nouveau-transition-hack.patch: drop, supported with driver pixmaps anyway

* Wed Sep 09 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-8.20090904git2b5ec6a
- nouveau-tile7000.patch: workaround some display corruption on G8x

* Fri Sep 04 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-7.20090904git2b5ec6a
- fix cursor being left enabled on wrong display

* Thu Aug 27 2009 Adam Jackson <ajax@redhat.com> 0.0.15-6.20090820git569a17a
- nouveau-bgnr.patch: Enable seamless plymouth->gdm transition.

* Fri Aug 21 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-5.20090820git569a17a
- a couple more minor fixes

* Thu Aug 20 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-4.20090819gitfe2b5e6
- various fixes from upstream, build pending new xorg-x11-server update

* Tue Aug 11 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-3.20090810git85b1c86
- wfb fixes, driver pixmaps enabled by default

* Wed Aug 05 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-2.20090803git712064e
- dri2 fixes, no wfb without kms, non-kms fb resize fixes, other misc fixes

* Tue Aug 04 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-1.20090803git619103a
- upstream update, misc fixes

* Tue Jul 28 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.15-0.20090728git4d20547
- Update to latest upstream

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.0.14-4.20090717gitb1b2330
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-3.20090717gitb1b2330
- somehow missed updated patches to go on top

* Fri Jul 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-2.20090717gitb1b2330
- build fixes for recent X changes

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1:0.0.14-1.20090701git6d14327.1
- ABI bump

* Mon Jul 7 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-1.20090701git6d14327
- update from upstream + bring back additional features found in F11

* Fri Jun 26 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.14-0.20090625gitc0bf670
- rebase onto latest upstream.  missing some features that were patched into
  F11, they'll come back soon.

* Fri Apr 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-29.20090417gitfa2f111
- avoid post-beta hangs experienced by many people (rh#495764, rh#493222).
  - the bug here was relatively harmless, but exposed a more serious issue
    which has been fixed in libdrm-2.4.6-6.fc11
- kms: speed up transitions, they could take a couple of seconds previously
- framebuffer resize support (rh#495838, rh#487356, lots of dups)

* Wed Apr 15 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-27.20090413git7100c06
- fix rh#495843

* Mon Apr 13 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-26.20090413git7100c06
- nouveau-fedora.patch: split out into indivdual functionality
- nv50: disable acceleration on NVAx chipsets, it won't work properly yet
- drop nouveau-eedid.patch, it's upstream now

* Wed Apr 08 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-25.20090408gitd8545e6
- correct logic error in vbios parser (rh#493981)

* Wed Apr 08 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-24.20090408git960a5c8
- modify nv50 ddc regs again, fix kms edid property

* Tue Apr 07 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-23.20090407git11451ca
- upstream update: rh#492399, nv50 PROM fixes

* Sat Apr 04 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-22.20090404git836d985
- use consistent connector names across all modesetting paths
- rh#493981

* Fri Apr 03 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-21.20090403git11be9a9
- upstream update, loads of modesetting fixes
- rh#492819, rh#492427, rh#492289, rh#492289

* Mon Mar 30 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-20.20090330git9d46930
- xv bugfix

* Mon Mar 30 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-19.20090330git9213c39
- fix rh#492239, and various modesetting changes
- nouveau-eedid.patch: remove nv50 hunk, is upstream now

* Fri Mar 27 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-18.20090327gitf1907dc
- nv50: add default modes to mode pool for lvds panels (rh#492360)
- kms: fix getting edid blob from kernel

* Fri Mar 27 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-17.20090327gitf431e20
- fix partially obscured xv rendering without compmgr (rh#492227,rh#492229,rh#492428)
- fix crash when rotation requested (fdo#20848)
- additional sanity checks for kernel modesetting enabled

* Thu Mar 26 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-16.20090326git01cee29
- update, should fix rh#497173

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-15.20090324git4067ab4
- more ppc build fixes

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-14.20090323git3063486
- fix ppc build

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-13.20090323gitd80fe78
- modesetting fixes, should handle rh#487456

* Mon Mar 23 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-12.20090318git3e7fa97
- upstream update, various fixes to pre-nv50 modesetting, cleanups

* Fri Mar 13 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-11.20090313git79d23d8
- kms: dpms fixes
- kms: nicer reporting of output properties to users
- improve init paths, more robust
- support for multiple xservers (fast user switching)

* Tue Mar 10 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-10.20090310git8f9a580
- upstream update, should fix #455194

* Mon Mar 09 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-9.20090309gited9bd88
- upstream update, fixes
- store used vbios image in /var/run, will potentially help debugging later

* Thu Mar 05 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-8.20090305git42f99e6
- upstream update, fixes
- kms: support gamma and dpms calls
- kms: nicer transition to gdm from plymouth

* Mon Mar 02 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-7.20090302gite6c3b98
- upstream update, fixes

* Fri Feb 27 2009 Adam Jackson <ajax@redhat.com> 0.0.12-6.20090224gitd91fc78
- nouveau-eedid.patch: Do EEDID.

* Tue Feb 24 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-5.20090224gitd91fc78
- improve description of package

* Tue Feb 24 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-4.20090224gitd91fc78
- new upstream snapshot

* Tue Feb 17 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-1.20090216git7b25a30
- fixes from upstream
- append git version to tarball filename

* Mon Feb 16 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-1.20090213git2573c06
- latest snapshot
- add patches to improve G80/G90 desktop performance 

* Sat Feb 7 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-3.20090205git945f0cb
- build with kms paths enabled, so things don't blow up with kms turned on

* Thu Feb 5 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.12-1.20090205git945f0cb
- latest snapshot - kernel interface 0.0.12

* Tue Feb 03 2009 Kyle McMartin <kyle@redhat.com> 0.0.11-2.20090106git133c1a5
- add build-dep on mesa (missing GL/gl.h due to glxint.h)

* Tue Jan 13 2009 Ben Skeggs <bskeggs@redhat.com> 0.0.11-1.20090106git133c1a5
- update to latest snapshot

* Wed Nov 19 2008 Dave Airlie <airlied@redhat.com> 0.0.11-1.20081119git65b956f
- update to latest upstream snapshot

* Tue Sep 02 2008 Dave Airlie <airlied@redhat.com> 0.0.11-1.20080902git6dd8ad4
- update to snapshot with new kernel interface 0.0.11

* Tue May 20 2008 Dave Airlie <airlied@redhat.com> 0.0.10-3.20080520git9c1d87f
- update to latest snapshot - enables randr12

* Tue Apr 08 2008 Dave Airlie <airlied@redhat.com> 0.0.10-2.20080408git0991281
- Update to latest snapshot

* Tue Mar 11 2008 Dave Airlie <airlied@redhat.com> 1:0.0.10-1.20080311git460cb26
- update to latest snapshot

* Fri Feb 29 2008 Dave Airlie <airlied@redhat.com> 1:0.0.10-1.20080221git5db7920
- Initial package for nouveau driver.
