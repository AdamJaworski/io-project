from llama_cpp import Llama
from common.path_manager import PathManager

current_n_ctx = 65536
llm = Llama(model_path=str(PathManager().model_llama / 'model.gguf'), n_ctx=current_n_ctx, verbose=False)

def double_n_ctx():
    global llm, current_n_ctx
    current_n_ctx *= 2
    llm = Llama(model_path=str(PathManager().model_llama / 'model.gguf'), n_ctx=current_n_ctx, verbose=False)