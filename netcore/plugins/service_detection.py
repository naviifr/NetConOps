from .base_class import BasePlugin
from core.models import ScanContext
import plugins.support.signatures as sign


class Service_Detection(BasePlugin):
    name = 'service'
    dependency = 'tcp'

    def execute(self, context: ScanContext):

        try:
            plg_confidence = self.collect_data(context.result.plg_data)
            results = self.infer(plg_confidence, context.job.port)
            self.write_result(results, context.result.plg_data)

        except Exception as e:
                    context.result.error['service'] = str(e)


    def collect_data(self, plg_data: dict):

        def recursive_collection(dict_data: dict, temp_confidence):
            
            for key, value in dict_data.items():

                if isinstance(value, dict):
                    recursive_collection(value, temp_confidence)

                else:

                    plg_confidence.append((temp_confidence, value))

                    
        plg_confidence = []

        for key, value in plg_data.items():

            if key in sign.confidence:
                confidence = sign.confidence[key]
            else:
                confidence = 'low'

            if isinstance(value, dict):
                recursive_collection(value,confidence)
            
            else:
                plg_confidence.append((confidence, value))

        return plg_confidence


    def infer(self, plg_confidence: list, port):

        pattern = None
        result = []

        if plg_confidence:

             for i in plg_confidence:

                for j in sign.patterns:
                     pattern = j[0]
                     match = pattern.search(str(i[1]))

                     if match is not None:
                          result.append((i[0], j[1]))

        if len(plg_confidence) == 0 or len(result) == 0:

            for key, val in sign.common_ports.items():

                if port == key:
                     result.append(('low', val))

        return result

    def write_result(self, result_dict: list, context_plgdata):

        rating = 0
        service = ''
        confidence = ''
        
        if result_dict:
            for i in result_dict:
                 
                 if rating < sign.confidence_rating[i[0]]:
                      
                      rating = sign.confidence_rating[i[0]]
                      service = i[1]
                      confidence = i[0]

            context_plgdata['service'] = {
                                            'service': service,
                                            'confidence': confidence
                                            }