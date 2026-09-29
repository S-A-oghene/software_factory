from __future__ import annotations
import json, os, urllib.request
from dataclasses import dataclass

@dataclass
class ModelResponse:
    message: dict
    raw: dict|None=None

class Model:
    def complete(self,messages,tools): raise NotImplementedError

class MockModel(Model):
    def __init__(self): self.calls=0
    def complete(self,messages,tools):
        self.calls += 1
        if self.calls==1:
            return ModelResponse({'role':'assistant','content':'Use repository inspection, then make a minimal evidence-backed change.','tool_calls':[{'id':'m1','type':'function','function':{'name':'inspect_repository','arguments':'{}'}}]})
        return ModelResponse({'role':'assistant','content':'Deterministic mock completed the bounded interaction.'})

class OpenAICompatibleModel(Model):
    def __init__(self,base_url,api_key,model): self.base_url=base_url.rstrip('/'); self.api_key=api_key; self.model=model
    def complete(self,messages,tools):
        payload={'model':self.model,'messages':messages,'tools':tools,'temperature':0}
        req=urllib.request.Request(self.base_url+'/chat/completions',data=json.dumps(payload).encode(),method='POST',headers={'Authorization':'Bearer '+self.api_key,'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=180) as r: data=json.loads(r.read())
        return ModelResponse(((data.get('choices') or [{}])[0].get('message') or {'role':'assistant','content':''}),data)


def make_model(mode='mock'):
    if mode=='mock': return MockModel()
    if mode=='openai-compatible':
        key=os.getenv('MODEL_API_KEY',''); base=os.getenv('MODEL_BASE_URL',''); model=os.getenv('MODEL_NAME','')
        if not all([key,base,model]): raise RuntimeError('MODEL_API_KEY, MODEL_BASE_URL and MODEL_NAME are required')
        return OpenAICompatibleModel(base,key,model)
    raise ValueError(mode)
