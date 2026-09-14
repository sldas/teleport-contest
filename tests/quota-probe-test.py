#!/usr/bin/env python3
"""Synthetic quota responses only; no account reads or model calls."""
import importlib.util,pathlib,time,unittest
p=pathlib.Path(__file__).resolve().parent.parent/'ops/quota_probe.py'
s=importlib.util.spec_from_file_location('quota',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class QuotaTests(unittest.TestCase):
 def response(self,used=35,reset=None):return {'result':{'rateLimits':{'limitId':'codex','primary':{'usedPercent':used,'resetsAt':reset or time.time()+3600,'windowDurationMins':300}}}}
 def test_auth_failure_not_zero(self):self.assertEqual(m.normalize({'error':{'message':'401 Unauthorized'}}),{'lookup_ok':False,'reason':'authentication_rejected'})
 def test_missing_usage_not_zero(self):self.assertFalse(m.normalize(self.response(None))['lookup_ok'])
 def test_expired_window(self):self.assertFalse(m.normalize(self.response(reset=1))['lookup_ok'])
 def test_nonfinite_usage(self):self.assertFalse(m.normalize(self.response(float('nan')))['lookup_ok'])
 def test_over_limit_valid(self):self.assertEqual(m.normalize(self.response(105))['windows'][0]['remaining_percent'],0)
 def test_valid_account_scope(self):self.assertEqual(m.normalize(self.response())['scope'],'account_not_project')
 def test_all_buckets(self):
  a=self.response()['result']['rateLimits'];r=m.normalize({'result':{'rateLimitsByLimitId':{'a':a,'b':a}}});self.assertEqual(len(r['windows']),2)
 def test_no_windows(self):self.assertFalse(m.normalize({'result':{}})['lookup_ok'])
if __name__=='__main__':unittest.main()
