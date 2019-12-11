def config_ssd_resnet_fpn(configs, config_params):
    
    model_config = configs['model']
    model_config.ssd.num_classes = config_params['num_classes']

    
    if config_params['width'] is not None:
        model_config.ssd.image_resizer.fixed_shape_resizer.width = config_params['width']

    if config_params['height'] is not None:
        model_config.ssd.image_resizer.fixed_shape_resizer.height = config_params['height']


    train_config = configs['train_config']
    train_config.batch_size = config_params['batch_size']
    train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.learning_rate_base = config_params['learning_rate']
    train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.warmup_learning_rate = config_params['learning_rate']/10

    if config_params['checkpoint_path'] is not None:
        train_config.fine_tune_checkpoint = config_params['checkpoint_path']

    return configs

