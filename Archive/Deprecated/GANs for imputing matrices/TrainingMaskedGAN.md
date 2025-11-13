# TrainingMaskedGAN
Please clone this: [https://github.com/Medial-EarlySign/MR_Projects/tree/main/ButWhy](https://github.com/Medial-EarlySign/MR_Projects/tree/main/ButWhy)
 
There is a python script called "channels_GAN\train_channels_GAN.py"
Example running command from directory with "train_channels_GAN.py":
 
Train scripts, generate 3 files
```bash
train_channels_GAN.py --rep ${TRAIN_REP} --get_mat --gpu "0" --gen_nhiddens 400,400,400 --disc_nhiddens 100,100,100 \
--gen_noise 0.01 --disc_noise 0.2 --gen_keep_prob 0.5 --disc_keep_prob 0.5 --gen_learning_rate 0.001 \
--disc_learning_rate 0.001 --max_auc_batch 1000 --disc_global_p 0.5 --gen_global_p 0.5 --cross_entropy_weight 0.5 \
--batch_size 1000 --csvs_freq 5000 --batch_num 100000 --n_dsteps 5 --n_gsteps 3 --round 1 --nout 50000 \
--work_output_dir ${output_directory} --samples ${SAMPLES_PATH} --model ${WORK_PATH}/base_model.bin --sub_sample 0
 
#disc_nhiddens  - discriminator hidden layers
#gen_nhiddens  - generator hidden layers
#model - to generate matrix with missing values to learn the GAN. this is trained model path, Or when no "get_mat", you can specify matrix directly in "data", "validation_data" argument.
```
 
Example output files:
W:\Users\Alon\But_Why\outputs\GAN\crc_gan_model.txt
there are 2 more files with additional suffix, when used, please specify the shortest file path without suffix
 
