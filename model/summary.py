from llama_cpp import Llama
from common.path_manager import PathManager

llm = Llama(model_path=str(PathManager().model_llama / 'model.gguf'), n_ctx=65536)