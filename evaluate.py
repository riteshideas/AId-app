from sgnlp.models.sentic_gcn.eval import SenticGCNEvaluator, SenticGCNBertEvaluator
from sgnlp.models.sentic_gcn.utils import parse_args_and_load_config, set_random_seed



cfg = parse_args_and_load_config()
if cfg.seed is not None:
    set_random_seed(cfg.seed)
evaluator = SenticGCNEvaluator(cfg) if cfg.model == "senticgcn" else SenticGCNBertEvaluator(cfg)
evaluator.evaluate()