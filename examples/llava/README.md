# LLaVA

Currently this implementation supports [llava-v1.5](https://huggingface.co/liuhaotian/llava-v1.5-7b) variants.

The pre-converted [7b](https://huggingface.co/mys/ggml_llava-v1.5-7b)
and [13b](https://huggingface.co/mys/ggml_llava-v1.5-13b)
models are available.

After API is confirmed, more models will be supported / uploaded.

## Usage
Build with cmake or run `make llava` to build it.

After building, run: `./llava` to see the usage. For example:

```sh
./llava -m llava-v1.5-7b/ggml-model-q5_k.gguf --mmproj llava-v1.5-7b/mmproj-model-f16.gguf --image path/to/an/image.jpg
```

**note**: A lower temperature like 0.1 is recommended for better quality. add `--temp 0.1` to the command to do so.

## Model conversion

- Clone `llava-v15-7b`` and `clip-vit-large-patch14-336`` locally:

```sh
git clone https://huggingface.co/liuhaotian/llava-v1.5-7b

git clone https://huggingface.co/openai/clip-vit-large-patch14-336
```

2. Use `llava-surgery.py` to split the LLaVA model to LLaMA and multimodel projector constituents:

```sh
python ./examples/llava/llava-surgery.py -m ../llava-v1.5-7b
```

3. Use `convert-image-encoder-to-gguf.py` to convert the LLaVA image encoder to GGUF:

```sh
python ./examples/llava/convert-image-encoder-to-gguf -m ../clip-vit-large-patch14-336 --llava-projector ../llava-v1.5-7b/llava.projector --output-dir ../llava-v1.5-7b
```

4. Use `convert.py` to convert the LLaMA part of LLaVA to GGUF:

```sh
python ./convert.py ../llava-v1.5-7b
```

Now both the LLaMA part and the image encoder is in the `llava-v1.5-7b` directory.

## Run Using the Web Interface
You can also utilize a web interface to perform inference.

**Prerequisite**: Make sure you have built the llava using cmake or running `make llava` as described above

**Dowload the Models**: Download both the preconvered [7B](https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q5_k.gguf) model and [mmproj](https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/mmproj-model-f16.gguf) files into the `models` folder



1. Install necessary web app dependencies
```sh
pip install streamlit==1.27.2
```
2. Launch the web user interface with the following command::
```sh
streamlit run --mml-model-path llava-v1.5-7b/ggml-model-q5_k.gguf --mproj-path llava-v1.5-7b/mmproj-model-f16.gguf 
```
Once the interface is up and running, you can easily upload your image and initiate the inference process. Access the app through your web browser at 
```sh
http://localhost:8501
```
If you don't specify a question, the app will use the default llava question. For a visual preview of the app, refer to the screenshot below:

![image](https://github.com/ggerganov/llama.cpp/assets/32692718/adcff621-4852-431c-8262-d2c3d5a05c3b)

## TODO

- [ ] Support server mode.
- [ ] Support non-CPU backend for the image encoding part.
- [ ] Support different sampling methods.
- [ ] Support more model variants.
