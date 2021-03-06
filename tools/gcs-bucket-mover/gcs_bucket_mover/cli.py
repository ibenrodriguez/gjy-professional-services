#!/usr/bin/env python2
# Copyright 2018 Google LLC. All rights reserved. Licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under
# the License.
#
# Any software provided by Google hereunder is distributed "AS IS", WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, and is not intended for production use.
"""Parses the command line and starts the script"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import textwrap

from gcs_bucket_mover import bucket_mover_service
from gcs_bucket_mover import bucket_mover_tester


def get_config():
    """Parses command line arguments.

    Args:
        None

    Returns:
        A "Namespace" object. See argparse.ArgumentParser.parse_args() for more details.
    """

    parser = argparse.ArgumentParser(
        description=
        'Moves a GCS bucket from one project to another, along with all objects and optionally'
        ' copying all other bucket settings.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        'bucket_name', type=str, help='The name of the bucket to be moved.')
    parser.add_argument(
        'source_project',
        type=str,
        help='The project id that the bucket is currently in.')
    parser.add_argument(
        'target_project',
        type=str,
        help='The project id that the bucket will be moved to.')
    parser.add_argument(
        '--test',
        action='store_true',
        help=textwrap.dedent('''\
        This will run a test of the tool to ensure all permissions are set up correctly and
        buckets can be moved between the two projects, using a randomly generated bucket.
        A fake bucket name will still need to be specified.'''))
    parser.add_argument(
        '--tempBucketName',
        type=str,
        help='The termporary bucket name to use in the target project.')
    parser.add_argument(
        '--location',
        type=str,
        help='Specify a different location for the target bucket.')
    parser.add_argument(
        '--storageClass',
        type=str,
        choices=[
            'MULTI_REGIONAL', 'NAM4', 'REGIONAL', 'STANDARD', 'NEARLINE',
            'COLDLINE', 'DURABLE_REDUCED_AVAILABILITY'
        ],
        help='Specify a different storage class for the target bucket.')
    parser.add_argument(
        '--skipEverything',
        action='store_true',
        help=
        'Only copies the bucket\'s storage class and location. Equivalent to setting every other'
        ' --skip parameter to True.')
    parser.add_argument(
        '--skipAcl',
        action='store_true',
        help='Don\'t replicate the ACLs from the source bucket.')
    parser.add_argument(
        '--skipCors',
        action='store_true',
        help='Don\'t copy the CORS settings from the source bucket.')
    parser.add_argument(
        '--skipDefaultObjectAcl',
        action='store_true',
        help='Don\'t copy the Default Object ACL from the source bucket.')
    parser.add_argument(
        '--skipIam',
        action='store_true',
        help='Don\'t replicate the IAM policies from the source bucket.')
    parser.add_argument(
        '--skipKmsKey',
        action='store_true',
        help='Don\'t copy the Default KMS Key from the source bucket.')
    parser.add_argument(
        '--skipLabels',
        action='store_true',
        help='Don\'t copy the Labels from the source bucket.')
    parser.add_argument(
        '--skipLogging',
        action='store_true',
        help='Don\'t copy the Logging settings from the source bucket.')
    parser.add_argument(
        '--skipLifecycleRules',
        action='store_true',
        help='Don\'t copy the Lifecycle Rules from the source bucket.')
    parser.add_argument(
        '--skipNotifications',
        action='store_true',
        help=
        'Don\'t copy the Cloud Pub/Sub notification setting from the source bucket.'
    )
    parser.add_argument(
        '--skipRequesterPays',
        action='store_true',
        help='Don\'t copy the Requester Pays setting from the source bucket.')
    parser.add_argument(
        '--skipVersioning',
        action='store_true',
        help='Don\'t copy the Versioning setting from the source bucket.')

    return parser.parse_args()


def main():
    """Get config and run either a test run or an actual move"""
    config = get_config()

    if config.test:
        test_bucket_name = bucket_mover_tester.set_up_test_bucket(config)
        config.bucket_name = test_bucket_name

    bucket_mover_service.move_bucket(config)
