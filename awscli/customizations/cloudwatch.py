# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from awscli.arguments import CustomArgument
from awscli.customizations.utils import validate_mutually_exclusive_handler

def register_cloudwatch_commands(event_handler):
    event_handler.register('building-command-table.cloudwatch', add_cloudwatch_commands)
    event_handler.register('operation-args-parsed.cloudwatch.get-metric-statistics', validate_mutually_exclusive_handler(
        ['start-time', 'end-time'], ['since', 'until']
    ))

def add_cloudwatch_commands(command_table, session, **kwargs):
    command_table['get-metric-statistics'] = GetMetricStatistics(session)

class GetMetricStatistics(CustomArgument):
    NAME = 'get-metric-statistics'
    DESCRIPTION = (
        'Gets CloudWatch statistics for the specified metric.'
    )
    ARG_TABLE = [
        {'name': 'namespace', 'required': True, 'help_text': 'The namespace of the metric.'},
        {'name': 'metric-name', 'required': True, 'help_text': 'The name of the metric.'},
        {'name': 'dimensions', 'action': 'append', 'help_text': 'The dimensions to filter on.'},
        {'name': 'start-time', 'required': False, 'help_text': 'The start time of the logs period.'},
        {'name': 'end-time', 'required': False, 'help_text': 'The end time of the logs period.'},
        {'name': 'since', 'required': False, 'help_text': 'The start time of the logs period with human readable format.'},
        {'name': 'until', 'required': False, 'help_text': 'The end time of the logs period with human readable format.'},
        {'name': 'period', 'required': True, 'help_text': 'The period in seconds.'},
        {'name': 'statistics', 'required': True, 'help_text': 'The statistics to return.'},
        {'name': 'unit', 'required': True, 'help_text': 'The unit of the metric.'},
    ]

    def __init__(self, session):
        super(GetMetricStatistics, self).__init__(session)

    def _run_main(self, args, parsed_globals):
        self.get_metric_statistics(args, parsed_globals)

    def get_metric_statistics(self, args, parsed_globals):
        import decimal
        import datetime
        import dateutil.tz
        import dateutil.parser
        import botocore

        session = self._session
        client = session.create_client('cloudwatch', region_name=parsed_globals.region)
        # client.get_paginator('get_metric_statistics')

        # Convert the start and end times to datetime objects
        start_time = dateutil.parser.parse(args.start_time)
        end_time = dateutil.parser.parse(args.end_time)

        # Convert the period to an integer
        period = int(args.period)

        # Convert the unit to a string
        unit = str(args.unit)

        # Convert the dimensions to a list of dictionaries
        dimensions = []
        # for dimension in args.dimensions:
        #     dimension_dict = {}
        #     dimension_dict['Name'] = dimension[0]
        #     dimension_dict['Value'] = dimension[1]
        #     dimensions.append(dimension_dict)
        
        # Convert the statistics to a list
        statistics = []
        if args.statistics:
            statistics = args.statistics.split(',')

        # Get the statistics
        response = client.get_metric_statistics(
            Namespace=args.namespace,
            MetricName=args.metric_name,
            Dimensions=dimensions,
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=statistics,
            Unit=unit
        )
        print(response)
        