#
# crash core analysis suite
#
Summary: Kernel crash and live system analysis utility
Name: crash
Version: 7.1.0
Release: 8%{?dist}
License: GPLv3
Group: Development/Debuggers
Source: http://people.redhat.com/anderson/crash-%{version}.tar.gz
URL: http://people.redhat.com/anderson
ExclusiveOS: Linux
ExclusiveArch: %{ix86} ia64 x86_64 ppc64 s390 s390x
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)
BuildRequires: ncurses-devel zlib-devel lzo-devel snappy-devel bison
Requires: binutils
Patch0: lzo_snappy.patch
Patch1: sadump_16TB.patch
Patch2: handle_corrupt_pid_hash.patch
Patch3: flattened_format_fixes.patch
Patch4: timer_command_fix.patch
Patch5: fix_sadump_read_failures.patch
Patch6: sadump_read_excluded_pages.patch
Patch7: lkcd_trace.patch
Patch8: backport_of_github_d833432f_kpti_trampoline.patch

%description
The core analysis suite is a self-contained tool that can be used to
investigate either live systems, kernel core dumps created from the
netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch
offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Requires: %{name} = %{version}, zlib-devel
Summary: kernel crash and live system analysis utility
Group: Development/Debuggers

%description devel
The core analysis suite is a self-contained tool that can be used to
investigate either live systems, kernel core dumps created from the
netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch
offered by Mission Critical Linux, or the LKCD kernel patch.

%prep
%setup -n %{name}-%{version} -q
%patch0 -p1 -b lzo_snappy.patch
%patch1 -p1 -b sadump_16TB.patch
%patch2 -p1 -b handle_corrupt_pid_hash.patch
%patch3 -p1 -b flattened_format_fixes.patch
%patch4 -p1 -b timer_command_fix.patch
%patch5 -p1 -b fix_sadump_read_failures.patch
%patch6 -p1 -b sadump_read_excluded_pages.patch
%patch7 -p1 -b lkcd_trace.patch
%patch8 -p1 -b backport_of_github_d833432f_kpti_trampoline.patch

%build
make RPMPKG="%{version}-%{release}" CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_mandir}/man8
cp -p crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/crash
%{_mandir}/man8/crash.8*
%doc README COPYING3

%files devel
%defattr(-,root,root,-)
%{_includedir}/*

%changelog
* Wed Apr 18 2018 Dave Anderson <anderson@redhat.com> - 7.1.0-8.el6
- Add support for KPTI entry trampoline stack
  Resolves: rhbz#1567738

* Thu Apr 12 2018 Dave Anderson <anderson@redhat.com> - 7.1.0-7.el6
- LKCD backtrace fixes
  Resolves: rhbz#1552558

* Wed Feb 03 2016 Dave Anderson <anderson@redhat.com> - 7.1.0-6.el6
- crash fails to read excluded pages by default on sadump-related formats
  Resolves: rhbz#1304262

* Mon Nov 23 2015 Dave Anderson <anderson@redhat.com> - 7.1.0-5.el6
- crash fails to read or wrongly reads some parts of memory in sadump vmcore format
  Resolves: rhbz#1283000

* Mon Nov  2 2015 Dave Anderson <anderson@redhat.com> - 7.1.0-4.el6
- Fixes for the handling of truncated/incomplete flat-format vmcores, which
  may cause the session to hang during initialization.
  Resolves: rhbz#1231976
- Fix for the "timer" command, which may fail with the error message
  "timer: cannot allocate any more memory!" when run on a kernel with
  an extremely large number of cpus.
  Resolves: rhbz#1238403

* Tue Apr 21 2015 Dave Anderson <anderson@redhat.com> - 7.1.0-3.el6
- Fortify the error handling of task gathering from the pid_hash[]
  chains during session initialization to prevent an endless loop if
  data structures have been corrupted.
  Resolves: rhbz#1208557

* Tue Mar 10 2015 Dave Anderson <anderson@redhat.com> - 7.1.0-2.el6
- Support new sadump format that can represent more than 16 TB physical memory space
  Resolves: rhbz#1195596

* Tue Feb 10 2015 Dave Anderson <anderson@redhat.com> - 7.1.0-1.el6
- Rebase
  Resolves: rhbz#1111357

* Wed Oct 23 2013 Dave Anderson <anderson@redhat.com> - 6.1.0-5.el6
- Fix read return error in compressed_kdump_46bit_support.patch (coverity)
  Resolves: rhbz#1006622

* Tue Oct 22 2013 Dave Anderson <anderson@redhat.com> - 6.1.0-4.el6
- Compressed kdump 46-bit physical memory support
  Resolves: rhbz#1006622
- Fix incorrect backtrace for dumps taken with "virsh dump --memory-only"
  Resolves: rhbz#1017930
- Fix cpu number display on systems with more than 254 cpus
  Resolves: rhbz#1019483
 
* Mon Sep 09 2013 Dave Anderson <anderson@redhat.com> - 6.1.0-3.el6
- snappy compression support
  Resolves: rhbz#902141

* Thu May 23 2013 Dave Anderson <anderson@redhat.com> - 6.1.0-2.el6
- LZO compression support.
  Resolves: rhbz#902144

* Mon Oct  1 2012 Dave Anderson <anderson@redhat.com> - 6.1.0-1.el6
- Rebase to upstream version 6.1.0.
  Resolves: rhbz#840051

* Thu Aug 23 2012 Dave Anderson <anderson@redhat.com> - 6.0.9-1.el6
- Fix for "crash: cannot resolve: xtime" session invocation failure.
  Resolves: rhbz#843093
- Enhance "struct" command to accept -o option with an address argument.
  Resolves: rhbz#834260
- Rebase to upstream version 6.0.9.
- Support for compressed/filtered ppc64 firmware-assisted dump (fadump).
  Resolves: rhbz#840051

* Wed May  2 2012 Dave Anderson <anderson@redhat.com> - 6.0.4-2.el6
- Fix s390x "vm -p" to properly handle swapped-out and unmapped
  user pages.
- Fix s390x "bt -[tT]" on a live system.
  Resolves: rhbz#817247
  Resolves: rhbz#817248

* Mon Feb 27 2012 Dave Anderson <anderson@redhat.com> - 6.0.4-1.el6
- Rebase to upstream version 6.0.4.
  Resolves: rhbz#767257

* Tue Feb 14 2012 Dave Anderson <anderson@redhat.com> - 6.0.3-1.el6
- Support sadump dumpfile formats for Fujitsu Stand Alone Dump facility.
  Resolves: rhbz#736884
- Support s390x ELF-kdump and s390x compressed-kdump dumpfiles.
  Resolves: rhbz#738865 
- Display an early warning message if any part of the kernel has been 
  erased/filtered by the makedumpfile facility.
  Resolves: rhbz#739096
- Fix for the "runq" command for kernels that are configured with
  CONFIG_FAIR_GROUP_SCHED.
  Resolves: rhbz#754291
- Fix for the x86_64 "bt" command to handle a recursive entry into
  the NMI exception stack.
  Resolves: rhbz#768189
- Fix for an x86_64 "bt" command segmentation violation if the number
  of ELF_PRSTATUS notes in a compressed-kdump do not match the number
  of cpus running when the system crashed.
  Resolves: rhbz#782837 
- Rebase to upstream version 6.0.3.
  Resolves: rhbz#767257

* Mon Sep 19 2011 Dave Anderson <anderson@redhat.com> - 5.1.8-1.el6
- Rebase to upstream version 5.1.8.
  Resolves: rhbz#710193

* Wed Jul 13 2011 Dave Anderson <anderson@redhat.com> - 5.1.7-1.el6
- Fix for "kmem -[sS]" if NUMA node 0 has no memory associated with it.
  Resolves: rhbz#716931
- Fix for the x86_64 "bt" command stack transition error when a non-crashing
  CPU receives a NMI immediately after receiving an interrupt from another 
  source. 
  Resolves: rhbz#712214
- Fix for the handling of x86_64 compressed kdump dumpfiles where
  the crashing system contains more than 454 cpus.
  Resolves: rhbz#705142
- Added a new "--osrelease <dumpfile>" command line option that
  displays the OSRELEASE vmcoreinfo string from a kdump dumpfile.
  Resolves: rhbz#703467
- Update to the crash(8) man page and the associated "crash -h" output.
  Resolves: rhbz#695413
- Rebase to upstream version 5.1.7.
  Resolves: rhbz#710193

* Thu Mar 10 2011 Dave Anderson <anderson@redhat.com> - 5.1.1-2.el6
- Fix for x86 "bt" command to account for movement of ia32_sysenter_target()
  assembly function to a separate text section, and for the failure to
  resolve the backtrace of a non-active swapper task.
  Resolves: rhbz#682129
- Upstream equivalency with 5.1.3 patch.
  Resolves: rhbz#649070

* Mon Jan 10 2011 Dave Anderson <anderson@redhat.com> - 5.1.1-1.el6
- Add support for s390x ELF dumpfile format.  
  Resolves: rhbz#633449
- Add support for s390x compressed/filtered dumpfiles generated by 
  makedumpfile.
  Resolves: rhbz#637197
- Fix for the "bt" command with 2.6.27 and later x86_64 kernels to
  prevent the possible display of a an invalid "vgettimeofday" frame
  above the topmost "system_call_fastpath" frame, followed by two
  read errors indicating "bt: read error: kernel virtual address:
  ffffffffff600000  type: gdb_readmem_callback".
  Resolves: rhbz#637735
- Save the per-cpu register contents stored in the "cpu" devices of 
  x86_64 KVM dumpfiles, and use their contents for x86_64 backtrace RSP
  and RIP hooks in the case of KVM "live dumps" where the guest system 
  was not in a crashed state when the "virsh dump" operation was done
  on the KVM host.  If an active task was running in user space when 
  a live dump was taken, that will be indicated by the "bt" output, 
  along with the user-space register contents.  The x86_64 register set 
  saved for each cpu may be displayed with the "help -[D|n]" command.
- Fix for the x86_64 "bt" command to more correctly find the starting
  backtrace RIP and RSP hooks in KVM dumpfiles.  Without the patch,
  backtraces that should start in the interrupt or exception stacks
  were not being detected correctly.
  Resolves: rhbz#649050
- Fix to utilize the correct "cpu" device format in x86 KVM dumpfiles
  Without the patch, the x86 registers were read in a 32-bit format, 
  which is only true if the host machine was running a 32-bit kernel.
  With the patch, the format defaults to the 64-bit format, and is
  switched to the 32-bit format if it can be determined that the host
  machine was running a 32-bit kernel.
- Save the per-cpu register contents stored in the "cpu" devices of
  x86 KVM dumpfiles, and use their contents for x86 backtrace ESP and
  EIP hooks in the case of KVM "live dumps", i.e., where the guest
  system was not in a crashed state when the "virsh dump" operation
  was done on the KVM host.  If an active task was running in user
  space when a live dump was taken, that will be indicated by the
  "bt" output, along with the user-space register contents.  The saved
  x86 register set for each cpu may also be displayed with the
  "help -[D|n]" command.
- Fix for the x86 "bt" command to correctly find the starting backtrace
  EIP and ESP hooks for the active tasks in KVM dumpfiles where the
  kernel had crashed.
  Resolves: rhbz#649051
- Fix for the cpu count determination in crashed x86 KVM dumpfiles, 
  where the non-crashing cpus are marked offline in the kernel's
  cpu_online_mask by smp_stop_cpu().  Depending upon the cpu number
  of the crashing task, the cpu count may be set to a value that is
  less than the number of present cpus.
- Change to the manner in which the cpu count is determined for x86_64
  kernels.  SLES11 2.6.32 kernels delay the call to crash_kexec() until
  after smp_send_stop() is called by panic(), and so the cpu_online_map
  cannot be used for determining the cpu count.  With the patch, the
  cpu_present_map is used.
  Resolves: rhbz#649053
- Rebase to upstream version 5.1.1.
  Resolves: rhbz#649070

* Wed Aug 18 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-23.el6
- Additional support for QEMU/savevm ram device version 4 to only use
  "pc.ram" segments and to handle the 512MB I/O hole at e0000000.
  Resolves: rhbz#619758

* Wed Aug 11 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-22.el6
- Support for QEMU/savevm ram device version 4.
  Resolves: rhbz#619758

* Fri Jul 16 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-21.el6
- Implement support for x86 and x86_64 RHEL6 xen/pvops kernels, both live
  and xendumps.
  Resolves: rhbz#608779

* Wed Jun 30 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-20.el6
- Fix for x86_64 "bt" if kdump NMI occurs while in system_call but 
  prior to switching from per-thread user stack to kernel stack.
  Resolves: rhbz#608173
- Fix for x86 "bt" to recognize all kernel entry-points without having
  to hardwire their symbol names.
  Resolves: rhbz#608718

* Tue Jun 15 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-19.el6
- Support for RHEL5 KVM dump generated "virsh dump" on a RHEL6 host.
  Resolves: rhbz#603142

* Tue Jun  8 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-18.el6
- Fix for segmentation violation when "mach -m" is run on an x86 machine
  which has a BIOS-provided e820 map that contains an EFI-related memory
  type of E820_UNUSABLE.
  Resolves: rhbz#601128

* Thu Jun  3 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-17.el6
- Fix for x86 "bt" command when a crash is generated by a kernel module's
  init_module() function.
  Resolves: rhbz#596904
- Correct the error message for "dev -p" command.
  Resolves: rhbz#598716
- Fix to recognize new block and kvmclock devices in the qemu KVM dumpfile.
  Resolves: rhbz#597187

* Wed May 26 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-16.el6
- Fix compiler warnings generated when building with -O2.
  Resolves: rhbz#596154

* Fri May 21 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-15.el6
- Fix for an incorrect calculation of the physical base address from
  a xendump of a fully-virtualized x86_64 RHEL6 guest kernel.
  Resolves: rhbz#593107
- Fix for an incorrect calculation of the physical base address from
  a kvmdump of an x86_64 kernel that has a "_text" virtual address 
  higher than __START_KERNEL_map.
  Resolves: rhbz#593285

* Tue May  3 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-14.el6
- Fix for "cannot resolve stack trace" errors when a non-panicking
  active task is interrupted by the shutdown NMI either while it is
  creating the pt_regs exception frame, or just after the exception
  frame has been created but before the system call handler is called.
  Resolves: rhbz#588337
- Fix display of ppc64 processor speed at session invocation, and by the
  "sys" and "mach" commands.
  Resolves: rhbz#588353
- Change the ppc64 cpu count displayed by the initial system banner
  and by the "sys" and "mach" commands to be the number of cpus online.
  Resolves: rhbz#587760

* Fri Apr 23 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-13.el6
- Update to support the re-worked IBM kernel patch for ppc64 
  CONFIG_SPARSEMEM_VMEMMAP kernels that will store vmemmap page
  mapping information, (re-)enabling the crash utility to be able
  to access kernel page structures.
  Resolves: rhbz#546175
  Resolves: rhbz#546527

* Wed Apr 21 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-12.el6
- Fix for missing general protection fault exception frame in "bt" output.
  Resolves: rhbz#583151

* Tue Mar 30 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-11.el6
- Fix for potential "double free or corruption" glibc abort when 
  running "kmem -s" command on CONFIG_SLAB-configured RHEL6 kernels.
  Resolves: rhbz#576117
- Implemented support to recognize an IBM-proposed kernel patch for
  ppc64 CONFIG_SPARSEMEM_VMEMMAP kernels that will store vmemmap page
  mapping information, (re-)enabling the crash utility to be able to
  access kernel page structures.
  Resolves: rhbz#546175
  Resolves: rhbz#546527
- Fix for "swap" and "kmem -i" commands on big-endian ppc64 machines
  to account for size change of the swap_info_struct.flags member.
  Resolves: rhbz#577969

* Mon Mar 22 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-10.el6
- Fix for "irq: invalid structure member offset: irqaction_mask" error
  generated by "irq" command.
  Resolves: rhbz#575668
- Fix for session abort cause by "bt -e" on x86.
  Resolves: rhbz#575673
- Fix for reading dumpfiles generated by snap extension modules on 
  systems with single PT_LOAD segment that starts at a non-zero address.
  Resolves: rhbz#575804

* Fri Mar 19 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-9.el6
- Fix for incorrect module symbol value recalculation/modification 
  done by "mod -[sS]" command.
  Resolves: rhbz#575144

* Wed Mar 10 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-8.el6
- Add "bt" support for x86_64 kernels configured with CONFIG_FRAME_POINTER.
  Resolves: rhbz#570909
- Fix to handle the loss of /dev/tty, such as when the network connection 
  hosting a crash session is killed.
  Resolves: rhbz#571782

* Wed Feb 10 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-7.el6
- Fix for very large xendump core files whose ELF sections are located
  beyond a file offset of 4GB.
  Resolves: rhbz#563542
- Additional fix for the "bt" command when run on offline s390/s390x 
  "swapper" idle tasks.
  Resolves: rhbz#559262

* Mon Feb 08 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-6.el6
- Fix for a gdb-7.0 regression that caused line numbers to fail with
  x86 (32-bit) base kernel text addresses. 
  Resolves: rhbz#562948

* Tue Feb 02 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-5.el6
- Fix for the "struct" and "union" commands when passed an address that
  is in a valid kernel virtual address region but is either unmapped or
  non-existent.  Without the patch, the following three error messages
  are displayed:
    struct <name> struct: invalid kernel virtual address: <kernel-address>  type: "gdb_readmem_callback"
    gdb called without error_hook: Cannot access memory at address <kernel-address>
    *** glibc detected *** crash: double free or corruption (!prev): <crash-address> ***
  followed by a backtrace and the crash utility memory map.  The session
  aborts at that point.  With the fix, the commands will fail gracefully
  after displaying error messages reporting that the kernel virtual
  address cannot be accessed.
  Resolves: rhbz#561048

* Wed Jan 27 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-4.el6
- Fix for x86, s390, s390x (and ia64) architectures to set the system
  cpu count equal to the highest cpu online plus one.  Without the
  patch, those architectures would use the number of online cpus as
  the system's total cpu count, which would be misleading when any
  offline cpu number was less than the highest online cpu number.
  Resolves: rhbz#559262
- Fix to recognize the symbol type change of per-cpu variables from
  'd' or 'D' to 'V' in 2.6.32 kernels.
  Resolves: rhbz#559251

* Thu Jan 21 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-3.el6
- Update swap-handling functionality to recognize the new swap_info
  array type and swap_info_struct structure changes introduced into 
  the 2.6.32-4.el6 kernel.
  Resolves: rhbz#555379

* Wed Jan 13 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-2.el6
- Eliminate invocation-time "input string too large" error messages
  when analyzing 32-bit x86 RHEL5 kernels.
  Resolves: rhbz#554477
- Fix to run with early RHEL6 kernels with glibc less than 2.11
  by forcing the use of the builtin mkstemps() function. 
  Resolves: rhbz#554493

* Thu Jan 07 2010 Dave Anderson <anderson@redhat.com> - 5.0.0-1.el6
- Rebased package to upstream version 5.0.0.
  Resolves: rhbz#528189
- Increment the built-in NR_CPUS value for x86_64 from 512 to 4096.
  Resolves: rhbz#513156
- Fix for the "bt" command on 2.6.29 and later x86_64 kernels to
  always recognize and display BUG()-induced exception frames.
  Resolves: rhbz#548789
- Fix for the "mount" command on 2.6.32 and later kernels.
  Resolves: rhbz#548791
- Fix for segmentation violation when running the "ps -r" command
  option on 2.6.25 or later kernels.
  Resolves: rhbz#549243
- Fix for 2.6.31 or later x86_64 CONFIG_NEED_MULTIPLE_NODES kernels
  running on systems that have multiple NUMA nodes.  By default, those
  kernels use the "page" (or "lpage") percpu memory allocators, which 
  utilize vmalloc space for percpu memory.
  Resolves: rhbz#540772

* Fri Sep 11 2009 Dave Anderson <anderson@redhat.com> - 4.0.9-2
  Bump version.

* Fri Sep 11 2009 Dave Anderson <anderson@redhat.com> - 4.0.9-1
- Update to upstream release, which allows the removal of the 
  Revision tag workaround, the crash-4.0-8.11-dwarf3.patch and 
  the crash-4.0-8.11-optflags.patch

* Sun Aug 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 4.0.8.11-2
- Fix reading of dwarf 3 DW_AT_data_member_location
- Use proper compiler flags

* Wed Aug 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 4.0.8.11-1
- Update to later upstream release
- Fix abuse of Revision tag

- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-9.7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-8.7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Dave Anderson <anderson@redhat.com> - 4.0-7.7.2
- Replace exclusive arch i386 with ix86.

* Thu Feb 19 2009 Dave Anderson <anderson@redhat.com> - 4.0-7.7.1
- Updates to this file per crash merge review
- Update to upstream version 4.0-7.7.  Full changelog viewable in:
    http://people.redhat.com/anderson/crash.changelog.html

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.0-7
- fix license tag

* Tue Apr 29 2008 Dave Anderson <anderson@redhat.com> - 4.0-6.3
- Added crash-devel subpackage
- Updated crash.patch to match upstream version 4.0-6.3

* Wed Feb 20 2008 Dave Anderson <anderson@redhat.com> - 4.0-6.0.5
- Second attempt at addressing the GCC 4.3 build, which failed due
  to additional ptrace.h includes in the lkcd vmdump header files.

* Wed Feb 20 2008 Dave Anderson <anderson@redhat.com> - 4.0-6.0.4
- First attempt at addressing the GCC 4.3 build, which failed on x86_64
  because ptrace-abi.h (included by ptrace.h) uses the "u32" typedef,
  which relies on <asm/types.h>, and include/asm-x86_64/types.h
  does not not typedef u32 as done in include/asm-x86/types.h.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.0-6.0.3
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Dave Anderson <anderson@redhat.com> - 4.0-5.0.3
- Updated crash.patch to match upstream version 4.0-5.0.

* Wed Aug 29 2007 Dave Anderson <anderson@redhat.com> - 4.0-4.6.2
- Updated crash.patch to match upstream version 4.0-4.6.

* Wed Sep 13 2006 Dave Anderson <anderson@redhat.com> - 4.0-3.3
- Updated crash.patch to match upstream version 4.0-3.3.
- Support for x86_64 relocatable kernels.  BZ #204557

* Mon Aug  7 2006 Dave Anderson <anderson@redhat.com> - 4.0-3.1
- Updated crash.patch to match upstream version 4.0-3.1.
- Added kdump reference to description.
- Added s390 and s390x to ExclusiveArch list.  BZ #199125
- Removed LKCD v1 pt_regs references for s390/s390x build.
- Removed LKCD v2_v3 pt_regs references for for s390/s390x build.

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 4.0-3
- rebuild

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.4
- Updated crash.patch such that <asm/page.h> is not #include'd
  by s390_dump.c; IBM did not make the file s390[s] only; BZ #192719

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.3
- Updated crash.patch such that <asm/page.h> is not #include'd
  by vas_crash.h; only ia64 build complained; BZ #191719

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.2
- Updated crash.patch such that <asm/segment.h> is not #include'd
  by lkcd_x86_trace.c; also for BZ #191719

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.1
- Updated crash.patch to bring it up to 4.0-2.26, which should 
  address BZ #191719 - "crash fails to build in mock"

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.0-2.18.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 04 2006 Dave Anderson <anderson@redhat.com> 4.0-2.18
- Updated source package to crash-4.0.tar.gz, and crash.patch
  to bring it up to 4.0-2.18.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 03 2005 Dave Anderson <anderson@redhat.com> 3.10-13
- Compiler error- and warning-related fixes for gcc 4 build.
- Update to enhance x86 and x86_64 gdb disassembly output so as to
  symbolically display call targets from kernel module text without
  requiring module debuginfo data.
- Fix hole where an ia64 vmcore could be mistakenly accepted as a
  usable dumpfile on an x86_64 machine, leading eventually to a
  non-related error message.
* Wed Mar 02 2005 Dave Anderson <anderson@redhat.com> 3.10-12
- rebuild (gcc 4)
* Thu Feb 10 2005 Dave Anderson <anderson@redhat.com> 3.10-9
- Updated source package to crash-3.10.tar.gz, containing
  IBM's final ppc64 processor support for RHEL4
- Fixes potential "bt -a" hang on dumpfile where netdump IPI interrupted
  an x86 process while executing the instructions just after it had entered
  the kernel for a syscall, but before calling the handler.  BZ #139437
- Update to handle backtraces in dumpfiles generated on IA64 with the
  INIT switch (functionality intro'd in RHEL3-U5 kernel).  BZ #139429
- Fix for handling ia64 and x86_64 machines booted with maxcpus=1 on
  an SMP kernel.  BZ #139435
- Update to handle backtraces in dumpfiles generated on x86_64 from the
  NMI exception stack (functionality intro'd in RHEL3-U5 kernel).
- "kmem -[sS]" beefed up to more accurately verify slab cache chains
  and report errors found.
- Fix for ia64 INIT switch-generated backtrace handling when
  init_handler_platform() is inlined into ia64_init_handler();
  properly handles both RHEL3 and RHEL4 kernel patches.
  BZ #138350
- Update to enhance ia64 gdb disassembly output so as to
  symbolically display call targets from kernel module
  text without requiring module debuginfo data.

* Wed Jul 14 2004 Dave Anderson <anderson@redhat.com> 3.8-5
- bump release for fc3

* Tue Jul 13 2004 Dave Anderson <anderson@redhat.com> 3.8-4
- Fix for gcc 3.4.x/gdb issue where vmlinux was mistakenly presumed non-debug 

* Fri Jun 25 2004 Dave Anderson <anderson@redhat.com> 3.8-3
- remove (harmless) error message during ia64 diskdump invocation when
  an SMP system gets booted with maxcpus=1
- several 2.6 kernel specific updates

* Thu Jun 17 2004 Dave Anderson <anderson@redhat.com> 3.8-2
- updated source package to crash-3.8.tar.gz 
- diskdump support
- x86_64 processor support 

* Mon Sep 22 2003 Dave Anderson <anderson@redhat.com> 3.7-5
- make bt recovery code start fix-up only upon reaching first faulting frame

* Fri Sep 19 2003 Dave Anderson <anderson@redhat.com> 3.7-4
- fix "bt -e" and bt recovery code to recognize new __KERNEL_CS and DS

* Wed Sep 10 2003 Dave Anderson <anderson@redhat.com> 3.7-3
- patch to recognize per-cpu GDT changes that redefine __KERNEL_CS and DS

* Wed Sep 10 2003 Dave Anderson <anderson@redhat.com> 3.7-2
- patches for netdump active_set determination and slab info gathering 

* Wed Aug 20 2003 Dave Anderson <anderson@redhat.com> 3.7-1
- updated source package to crash-3.7.tar.gz

* Wed Jul 23 2003 Dave Anderson <anderson@redhat.com> 3.6-1
- removed Packager, Distribution, and Vendor tags
- updated source package to crash-3.6.tar.gz 

* Fri Jul 18 2003 Jay Fenlason <fenlason@redhat.com> 3.5-2
- remove ppc from arch list, since it doesn't work with ppc64 kernels
- remove alpha from the arch list since we don't build it any more

* Fri Jul 18 2003 Matt Wilson <msw@redhat.com> 3.5-1
- use %%defattr(-,root,root)

* Tue Jul 15 2003 Jay Fenlason <fenlason@redhat.com>
- Updated spec file as first step in turning this into a real RPM for taroon.
- Wrote man page.
