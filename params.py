import os
import json
import jsbeautifier

class Params():
    def __init__(self, gui_params="params_gui") -> None:
        """
        Initialization of parameter class instance
        Args:
        """
        params_path = os.path.join("params", gui_params+".json")

        with open(params_path) as f:
            params = json.load(f)

        self.main = {}
        self.main["size"] = params["main"]["size"]
        self.main["pos"] = params["main"]["pos"]

        self.map = {}
        self.map["size"] = params["map"]["size"]
        self.map["pos"] = params["map"]["pos"]

        self.images = {}
        self.images["size"] = params["images"]["size"]
        self.images["pos"] = params["images"]["pos"]

        self.table = {}
        self.table["size"] = params["table"]["size"]
        self.table["pos"] = params["table"]["pos"]

        self.table_new_row = {}
        self.table_new_row["size"] = params["table_new_row"]["size"]
        self.table_new_row["pos"] = params["table_new_row"]["pos"]

        self.button_add_route = {}
        self.button_add_route["size"] = params["button_add_route"]["size"]
        self.button_add_route["pos"] = params["button_add_route"]["pos"]

        self.button_save = {}
        self.button_save["size"] = params["button_save"]["size"]
        self.button_save["pos"] = params["button_save"]["pos"]

        self.sort_combobox = {}
        self.sort_combobox["size"] = params["sort_combobox"]["size"]
        self.sort_combobox["pos"] = params["sort_combobox"]["pos"]

        self.entry_combobox = {}
        self.entry_combobox["size"] = params["entry_combobox"]["size"]
        self.entry_combobox["pos"] = params["entry_combobox"]["pos"]

        self.order_combobox = {}
        self.order_combobox["size"] = params["order_combobox"]["size"]
        self.order_combobox["pos"] = params["order_combobox"]["pos"]

    # def save(self, model):
    #     """
    #     Save parameters in json file
    #     """
    #     params = {}
    #     if self.args.model_type == "HolohoverGrey" or self.args.model_type == "Signal2Thrust":
    #         params["model"] = {  
    #             "init_center_of_mass": self.center_of_mass,
    #             "learned_center_of_mass": list(model.center_of_mass.detach().numpy().astype(float)),
    #             "init_mass": self.mass,
    #             "learned_mass": model.mass.detach().numpy().astype(float).item(),
    #             "init_inertia": self.inertia,
    #             "learned_inertia": model.inertia.detach().numpy().astype(float).item(),
    #         }

    #         params["model"]["init_signal2thrust"] = self.signal2thrust
    #         sig2thr_list = []
    #         for lin_fct in model.sig2thr_fcts:
    #             sig2thr_list.append(list(lin_fct.weight.detach().numpy().flatten().astype(float)))
    #         params["model"]["learned_signal2thrust"] = sig2thr_list
    #         params["model"]["thrust2signal"] = self.thrust2signal
    #         params["model"]["motor_distance"] = self.motor_distance
    #         params["model"]["motor_angle_offset"] = self.motor_angle_offset
    #         params["model"]["motor_angel_delta"] = self.motor_angel_delta
    #         params["model"]["init_motors_vec"] = model.initMotorVec(self).detach().numpy().tolist()
    #         params["model"]["learned_motors_vec"] = model.motors_vec.detach().numpy().tolist()
    #         params["model"]["init_motors_pos"] = model.initMotorPos(self).detach().numpy().tolist()
    #         params["model"]["learned_motors_pos"] = model.motors_pos.detach().numpy().tolist()
    #         params["model"]["tau_up"] = self.tau_up
    #         params["model"]["tau_dw"] = self.tau_dw
        
    #     # Serializing json
    #     options = jsbeautifier.default_options()
    #     options.indent_size = 4
    #     json_object = jsbeautifier.beautify(json.dumps(params), options)
        
    #     # Writing to sample.json
    #     with open(os.path.join(self.args.dir_path, "params_"+self.args.model_type+".json"), "w") as outfile:
    #         outfile.write(json_object)

