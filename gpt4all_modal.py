# REF:
# https://docs.gpt4all.io/gpt4all_modal.html
# https://github.com/modal-labs/modal-examples/blob/main/misc/gpt2_language_model.py
# ---
# args: ["--prompt", "What is AI?"]
# examples:
# MODEL_NAME="ggml-mpt-7b-instruct.bin" modal run gpt4all_modal.py --prompt "What is Flutter?"
# MODEL_NAME="ggml-gpt4all-j-v1.3-groovy.bin" modal run gpt4all_modal.py --prompt "What is Flutter?"
# ---
import modal
import os


def download_model():
    import gpt4all
    import os
    # you can use any model from https://gpt4all.io/models/models.json
    return gpt4all.GPT4All(os.environ["MODEL_NAME"])


image = modal.Image.debian_slim().env(
    {"MODEL_NAME": os.environ["MODEL_NAME"]}
).pip_install("gpt4all").run_function(download_model)
stub = modal.Stub("gpt4all", image=image)


@stub.cls(keep_warm=1)
class GPT4All:
    def __enter__(self):
        print("Downloading model")
        self.gpt4all = download_model()
        print("Loaded model")

    @modal.method()
    def generate(self, prompt: str):
        messages = [{"role": "user", "content": prompt}]
        completion = self.gpt4all.chat_completion(messages)
        return completion


@stub.local_entrypoint()
def main(prompt: str = None):
    model = GPT4All()
    print(model.generate.call(prompt=prompt or "What is AI?"))
