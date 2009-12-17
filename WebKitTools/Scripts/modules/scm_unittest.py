import os.path
from datetime import date
from modules.executive import Executive, run_command, ScriptError
from modules.scm import detect_scm_system, SCM, CheckoutNeedsUpdate, commit_error_handler
# FIXME: This should be unified into one of the executive.py commands!
        run_command(['svn', 'add', 'test_file'])
        run_command(['svn', 'commit', '--quiet', '--message', 'initial commit'])
        run_command(['svn', 'commit', '--quiet', '--message', 'second commit'])
        run_command(['svn', 'commit', '--quiet', '--message', 'third commit'])
        run_command(['svn', 'commit', '--quiet', '--message', 'fourth commit'])
        run_command(['svn', 'update'])
        run_command(['svnadmin', 'create', '--pre-1.5-compatible', test_object.svn_repo_path])
        run_command(['svn', 'checkout', '--quiet', test_object.svn_repo_url, test_object.svn_checkout_path])
        run_command(['rm', '-rf', test_object.svn_repo_path])
        run_command(['rm', '-rf', test_object.svn_checkout_path])
        input_process = subprocess.Popen(['echo', 'foo\nbar'], stdout=subprocess.PIPE, stderr=self.dev_null)
        self.assertEqual(run_command(['grep', 'bar'], input=input_process.stdout), "bar\n")
        self.assertEqual(run_command(['grep', 'bar'], input="foo\nbar"), "bar\n")
        self.assertRaises(ScriptError, run_command, ['grep', 'bar'], input=input_process.stdout)
        input_process = subprocess.Popen(['echo', 'foo\nbar'], stdout=subprocess.PIPE, stderr=self.dev_null) # grep shows usage and calls exit(2) when called w/o arguments.
        self.assertRaises(ScriptError, run_command, command_returns_non_zero, input=input_process.stdout)
        self.assertRaises(OSError, run_command, command_does_not_exist)
        self.assertRaises(OSError, run_command, command_does_not_exist, error_handler=Executive.ignore_error)
        self.assertRaises(ScriptError, run_command, command_returns_non_zero)
        # Check if returns error text:
        self.assertTrue(run_command(command_returns_non_zero, error_handler=Executive.ignore_error))
    def _shared_test_svn_apply_git_patch(self):
        self._setup_webkittools_scripts_symlink(self.scm)
        git_binary_addition = """diff --git a/fizzbuzz7.gif b/fizzbuzz7.gif
new file mode 100644
index 0000000000000000000000000000000000000000..64a9532e7794fcd791f6f12157406d90
60151690
GIT binary patch
literal 512
zcmZ?wbhEHbRAx|MU|?iW{Kxc~?KofD;ckY;H+&5HnHl!!GQMD7h+sU{_)e9f^V3c?
zhJP##HdZC#4K}7F68@!1jfWQg2daCm-gs#3|JREDT>c+pG4L<_2;w##WMO#ysPPap
zLqpAf1OE938xAsSp4!5f-o><?VKe(#0jEcwfHGF4%M1^kRs14oVBp2ZEL{E1N<-zJ
zsfLmOtKta;2_;2c#^S1-8cf<nb!QnGl>c!Xe6RXvrEtAWBvSDTgTO1j3vA31Puw!A
zs(87q)j_mVDTqBo-P+03-P5mHCEnJ+x}YdCuS7#bCCyePUe(ynK+|4b-3qK)T?Z&)
zYG+`tl4h?GZv_$t82}X4*DTE|$;{DEiPyF@)U-1+FaX++T9H{&%cag`W1|zVP@`%b
zqiSkp6{BTpWTkCr!=<C6Q=?#~R8^JfrliAF6Q^gV9Iup8RqCXqqhqC`qsyhk<-nlB
z00f{QZvfK&|Nm#oZ0TQl`Yr$BIa6A@16O26ud7H<QM=xl`toLKnz-3h@9c9q&wm|X
z{89I|WPyD!*M?gv?q`;L=2YFeXrJQNti4?}s!zFo=5CzeBxC69xA<zrjP<wUcCRh4
ptUl-ZG<%a~#LwkIWv&q!KSCH7tQ8cJDiw+|GV?MN)RjY50RTb-xvT&H

literal 0
HcmV?d00001

"""
        self.scm.apply_patch(self._create_patch(git_binary_addition))
        added = read_from_path('fizzbuzz7.gif')
        self.assertEqual(512, len(added))
        self.assertTrue(added.startswith('GIF89a'))
        self.assertTrue('fizzbuzz7.gif' in self.scm.changed_files())

        # The file already exists.
        self.assertRaises(ScriptError, self.scm.apply_patch, self._create_patch(git_binary_addition))

        git_binary_modification = """diff --git a/fizzbuzz7.gif b/fizzbuzz7.gif
index 64a9532e7794fcd791f6f12157406d9060151690..323fae03f4606ea9991df8befbb2fca7
GIT binary patch
literal 7
OcmYex&reD$;sO8*F9L)B

literal 512
zcmZ?wbhEHbRAx|MU|?iW{Kxc~?KofD;ckY;H+&5HnHl!!GQMD7h+sU{_)e9f^V3c?
zhJP##HdZC#4K}7F68@!1jfWQg2daCm-gs#3|JREDT>c+pG4L<_2;w##WMO#ysPPap
zLqpAf1OE938xAsSp4!5f-o><?VKe(#0jEcwfHGF4%M1^kRs14oVBp2ZEL{E1N<-zJ
zsfLmOtKta;2_;2c#^S1-8cf<nb!QnGl>c!Xe6RXvrEtAWBvSDTgTO1j3vA31Puw!A
zs(87q)j_mVDTqBo-P+03-P5mHCEnJ+x}YdCuS7#bCCyePUe(ynK+|4b-3qK)T?Z&)
zYG+`tl4h?GZv_$t82}X4*DTE|$;{DEiPyF@)U-1+FaX++T9H{&%cag`W1|zVP@`%b
zqiSkp6{BTpWTkCr!=<C6Q=?#~R8^JfrliAF6Q^gV9Iup8RqCXqqhqC`qsyhk<-nlB
z00f{QZvfK&|Nm#oZ0TQl`Yr$BIa6A@16O26ud7H<QM=xl`toLKnz-3h@9c9q&wm|X
z{89I|WPyD!*M?gv?q`;L=2YFeXrJQNti4?}s!zFo=5CzeBxC69xA<zrjP<wUcCRh4
ptUl-ZG<%a~#LwkIWv&q!KSCH7tQ8cJDiw+|GV?MN)RjY50RTb-xvT&H

"""
        self.scm.apply_patch(self._create_patch(git_binary_modification))
        modified = read_from_path('fizzbuzz7.gif')
        self.assertEqual('foobar\n', modified)
        self.assertTrue('fizzbuzz7.gif' in self.scm.changed_files())

        # Applying the same modification should fail.
        self.assertRaises(ScriptError, self.scm.apply_patch, self._create_patch(git_binary_modification))

        git_binary_deletion = """diff --git a/fizzbuzz7.gif b/fizzbuzz7.gif
deleted file mode 100644
index 323fae0..0000000
GIT binary patch
literal 0
HcmV?d00001

literal 7
OcmYex&reD$;sO8*F9L)B

"""
        self.scm.apply_patch(self._create_patch(git_binary_deletion))
        self.assertFalse(os.path.exists('fizzbuzz7.gif'))
        self.assertFalse('fizzbuzz7.gif' in self.scm.changed_files())

        # Cannot delete again.
        self.assertRaises(ScriptError, self.scm.apply_patch, self._create_patch(git_binary_deletion))

    @staticmethod
    def _set_date_and_reviewer(changelog_entry):
        # Joe Cool matches the reviewer set in SCMTest._create_patch
        changelog_entry = changelog_entry.replace('REVIEWER_HERE', 'Joe Cool')
        # svn-apply will update ChangeLog entries with today's date.
        return changelog_entry.replace('DATE_HERE', date.today().isoformat())

    def test_svn_apply(self):
        first_entry = """2009-10-26  Eric Seidel  <eric@webkit.org>

        Reviewed by Foo Bar.

        Most awesome change ever.

        * scm_unittest.py:
"""
        intermediate_entry = """2009-10-27  Eric Seidel  <eric@webkit.org>

        Reviewed by Baz Bar.

        A more awesomer change yet!

        * scm_unittest.py:
"""
        one_line_overlap_patch = """Index: ChangeLog
===================================================================
--- ChangeLog	(revision 5)
+++ ChangeLog	(working copy)
@@ -1,5 +1,13 @@
 2009-10-26  Eric Seidel  <eric@webkit.org>

+        Reviewed by NOBODY (OOPS!).
+
+        Second most awsome change ever.
+
+        * scm_unittest.py:
+
+2009-10-26  Eric Seidel  <eric@webkit.org>
+
         Reviewed by Foo Bar.

         Most awesome change ever.
"""
        one_line_overlap_entry = """DATE_HERE  Eric Seidel  <eric@webkit.org>

        Reviewed by REVIEWER_HERE.

        Second most awsome change ever.

        * scm_unittest.py:
"""
        two_line_overlap_patch = """Index: ChangeLog
===================================================================
--- ChangeLog	(revision 5)
+++ ChangeLog	(working copy)
@@ -2,6 +2,14 @@

         Reviewed by Foo Bar.

+        Second most awsome change ever.
+
+        * scm_unittest.py:
+
+2009-10-26  Eric Seidel  <eric@webkit.org>
+
+        Reviewed by Foo Bar.
+
         Most awesome change ever.

         * scm_unittest.py:
"""
        two_line_overlap_entry = """DATE_HERE  Eric Seidel  <eric@webkit.org>

        Reviewed by Foo Bar.

        Second most awsome change ever.

        * scm_unittest.py:
"""
        write_into_file_at_path('ChangeLog', first_entry)
        run_command(['svn', 'add', 'ChangeLog'])
        run_command(['svn', 'commit', '--quiet', '--message', 'ChangeLog commit'])

        # Patch files were created against just 'first_entry'.
        # Add a second commit to make svn-apply have to apply the patches with fuzz.
        changelog_contents = "%s\n%s" % (intermediate_entry, first_entry)
        write_into_file_at_path('ChangeLog', changelog_contents)
        run_command(['svn', 'commit', '--quiet', '--message', 'Intermediate commit'])

        self._setup_webkittools_scripts_symlink(self.scm)
        self.scm.apply_patch(self._create_patch(one_line_overlap_patch))
        expected_changelog_contents = "%s\n%s" % (self._set_date_and_reviewer(one_line_overlap_entry), changelog_contents)
        self.assertEquals(read_from_path('ChangeLog'), expected_changelog_contents)

        self.scm.revert_files(['ChangeLog'])
        self.scm.apply_patch(self._create_patch(two_line_overlap_patch))
        expected_changelog_contents = "%s\n%s" % (self._set_date_and_reviewer(two_line_overlap_entry), changelog_contents)
        self.assertEquals(read_from_path('ChangeLog'), expected_changelog_contents)

        run_command(['svn', 'add', 'test_dir'])
        write_into_file_at_path(create_patch_path, '#!/bin/sh\necho $PWD') # We could pass -n to prevent the \n, but not all echo accept -n.
        self.assertEqual("%s\n" % os.path.realpath(scm.checkout_root), patch_contents) # Add a \n because echo adds a \n.
        patch = self._create_patch(run_command(['svn', 'diff', '-r4:3']))
        patch = self._create_patch(run_command(['svn', 'diff', '-r2:4']))
    def test_svn_apply_git_patch(self):
        self._shared_test_svn_apply_git_patch()
        run_command(['rm', '-rf', self.git_checkout_path])
        run_command(['svn', 'commit', '--message', 'commit to conflict with git commit'], cwd=self.svn_checkout_path)
        run_command(['git', 'commit', '-a', '-m', 'commit to be thrown away by rebase abort'])
        expected_commits += reversed(run_command(['git', 'rev-list', commit_range]).splitlines())
        patch = self._create_patch(run_command(['git', 'diff', 'HEAD..HEAD^']))
        patch = self._create_patch(run_command(['git', 'diff', 'HEAD~2..HEAD']))
    def test_svn_apply_git_patch(self):
        self._shared_test_svn_apply_git_patch()

    def test_create_binary_patch(self):
        # Create a git binary patch and check the contents.
        scm = detect_scm_system(self.git_checkout_path)
        test_file_name = 'binary_file'
        test_file_path = os.path.join(self.git_checkout_path, test_file_name)
        file_contents = ''.join(map(chr, range(256)))
        write_into_file_at_path(test_file_path, file_contents)
        run_command(['git', 'add', test_file_name])
        patch = scm.create_patch()
        self.assertTrue(re.search(r'\nliteral 0\n', patch))
        self.assertTrue(re.search(r'\nliteral 256\n', patch))

        # Check if we can apply the created patch.
        run_command(['git', 'rm', '-f', test_file_name])
        self._setup_webkittools_scripts_symlink(scm)
        self.scm.apply_patch(self._create_patch(patch))
        self.assertEqual(file_contents, read_from_path(test_file_path))

        # Check if we can create a patch from a local commit.
        write_into_file_at_path(test_file_path, file_contents)
        run_command(['git', 'add', test_file_name])
        run_command(['git', 'commit', '-m', 'binary diff'])
        patch_from_local_commit = scm.create_patch_from_local_commit('HEAD')
        self.assertTrue(re.search(r'\nliteral 0\n', patch_from_local_commit))
        self.assertTrue(re.search(r'\nliteral 256\n', patch_from_local_commit))
        patch_since_local_commit = scm.create_patch_since_local_commit('HEAD^1')
        self.assertTrue(re.search(r'\nliteral 0\n', patch_since_local_commit))
        self.assertTrue(re.search(r'\nliteral 256\n', patch_since_local_commit))
        self.assertEqual(patch_from_local_commit, patch_since_local_commit)

