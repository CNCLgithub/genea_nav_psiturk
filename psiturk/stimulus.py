import json
import os

from collections import defaultdict
from random import randint
from time import strftime, gmtime


class Paths:
    @staticmethod
    def get_root_dir_path():
        return os.path.dirname(os.path.dirname(__file__))

    @staticmethod
    def get_psiturk_static_dir_path():
        return os.path.join(Paths.get_root_dir_path(), "psiturk", "static")

    @staticmethod
    def get_json_data_dir_path():
        return os.path.join(Paths.get_psiturk_static_dir_path(), "data")

    @staticmethod
    def get_stimuli_videos_dir_path():
        return os.path.join(Paths.get_psiturk_static_dir_path(), "stimuli_videos")


class FileUtils:
    @staticmethod
    def get_files_in_directory(dir_path, is_sorted=True):
        try:
            return_list = list(filter(os.path.isfile, [os.path.join(dir_path, i) for i in os.listdir(dir_path)]))
            if is_sorted:
                return sorted(return_list)
            return return_list
        except Exception as e:
            print("ERROR: issue in retrieving files within directory " + dir_path)
            print(str(e))

    @staticmethod
    def get_basename(filepath, is_attached=True):
        if is_attached:
            return os.path.basename(filepath)
        return os.path.splitext(os.path.basename(filepath))


class Stimulus:
    def __init__(self, stimulus_id):
        self.stimulus_id = stimulus_id
        self.stimulus_video_name = None

    def set_stimulus_video_name(self, stimulus_video_name):
        self.stimulus_video_name = stimulus_video_name

    def get_stimulus_id(self):
        return self.stimulus_id

    def get_stimulus_video_name(self):
        return self.stimulus_video_name


class JsonWriter:
    PRACTICE = "practice"
    STIMULUS = "stimulus"

    TRIAL_ID = "trial_id"
    TRIAL_VIDEO_NAME = "trial_video_name"

    def __init__(self, practice_list, stimulus_list):
        self.json_object = self._get_practice_stimulus_dict(practice_list, stimulus_list)

    def _get_stimulus_dict(self, trial_id, trial_video_name):
        returned_dict = dict()
        returned_dict[self.TRIAL_ID] = trial_id
        returned_dict[self.TRIAL_VIDEO_NAME] = trial_video_name
        return returned_dict

    def _get_practice_stimulus_dict(self, practice_list, stimulus_list):
        returned_dict = dict()

        practice_array = []
        for stimulus in practice_list:
            practice_array.append(self._get_stimulus_dict(stimulus.get_stimulus_id(),
                                                          stimulus.get_stimulus_video_name()))

        stimuli_array = []
        for stimulus in stimulus_list:
            stimuli_array.append(self._get_stimulus_dict(stimulus.get_stimulus_id(),
                                                         stimulus.get_stimulus_video_name()))

        returned_dict[self.PRACTICE] = practice_array
        returned_dict[self.STIMULUS] = stimuli_array
        return returned_dict

    def get_json_string(self):
        return json.dumps(self.json_object, indent=2)

    @staticmethod
    def generate_json_condition_file(practice_list, stimulus_list):
        json_string = JsonWriter(practice_list, stimulus_list).get_json_string()

        with open(os.path.join(Paths.get_json_data_dir_path(), 'condition_list.json'), 'w') as cond_file:
            cond_file.write(json_string)
            cond_file.close()

        curr_time = strftime("_%m_%d_T_%H_%M_%S", gmtime())
        with open(os.path.join(Paths.get_json_data_dir_path(), 'condition_list' + curr_time + '.json'), 'w') as outfile:
            outfile.write(json_string)
            outfile.close()


def sample_exp_stimuli(video_filepaths_lists):
    stim_type_to_stim_filepath_dict = defaultdict(list)

    for video_filepath in video_filepaths_lists:
        stim_filename = FileUtils.get_basename(video_filepath, False)[0]

        stimuli_tex = stim_filename.split("_")[1]
        stimuli_num = int(stim_filename.split("_")[2])

        if stimuli_num == 0:  # practice platforms
            stim_type_to_stim_filepath_dict["p" + "_" + stimuli_tex].append(video_filepath)
        elif stimuli_num == 5:  # longest path
            stim_type_to_stim_filepath_dict["0" + "_" + stimuli_tex].append(video_filepath)
        elif stimuli_num % 5 == 2 or stimuli_num % 5 == 3 or stimuli_num % 5 == 4:  # similar triplets
            stim_type_to_stim_filepath_dict[str(stimuli_num // 5 * 2 + 1) + "_" + stimuli_tex].append(video_filepath)
        elif stimuli_num > 1 and stimuli_num % 5 == 1:  # triplets of the same platform
            stim_type_to_stim_filepath_dict[str(stimuli_num // 5 * 2) + "_" + stimuli_tex].append(video_filepath)

    return stim_type_to_stim_filepath_dict


def smart_shuffle_stim_type_dict(stim_type_dict):
    return_stim_type_list = []

    stim_type_list = [stim_type for stim_type in list(stim_type_dict.keys()) if not stim_type.startswith("p")]
    remaining_list = stim_type_list.copy()

    prev_prev_stim_num = None
    prev_prev_stim_tex = None
    prev_stim_num = None
    prev_stim_tex = None

    tries = 1
    while len(return_stim_type_list) < len(stim_type_list):
        sample_stim_type = remaining_list[randint(0, len(remaining_list) - 1)]

        stim_num = sample_stim_type.split("_")[0]
        stim_tex = sample_stim_type.split("_")[1]

        tries += 1
        if tries > 10:
            return smart_shuffle_stim_type_dict(stim_type_dict)

        if prev_stim_num == stim_num and prev_prev_stim_num == stim_num:
            continue

        if prev_stim_tex == stim_tex and prev_prev_stim_tex == stim_tex:
            continue

        prev_prev_stim_num = prev_stim_num
        prev_prev_stim_tex = prev_stim_tex
        prev_stim_num = stim_num
        prev_stim_tex = stim_tex

        return_stim_type_list.append(sample_stim_type)
        remaining_list.remove(sample_stim_type)

        tries = 1

    return return_stim_type_list


def make_condition_file():
    stim_type_dict = sample_exp_stimuli(FileUtils.get_files_in_directory(Paths.get_stimuli_videos_dir_path()))

    practice_list = []
    stim_num = 1
    for stim_type, stim_filepath_list in stim_type_dict.items():
        if stim_type.startswith("p"):
            for stim_filepath in stim_filepath_list:
                stimulus = Stimulus(stim_num)
                stimulus.set_stimulus_video_name(os.path.basename(stim_filepath))
                practice_list.append(stimulus)
                stim_num += 1

    stimulus_list = []
    stim_num = 1

    for stim_type in smart_shuffle_stim_type_dict(stim_type_dict):
        if stim_type.startswith("p"):
            continue

        stim_filepath = stim_type_dict[stim_type][randint(0, len(stim_type_dict[stim_type]) - 1)]

        stimulus = Stimulus(stim_num)
        stimulus.set_stimulus_video_name(os.path.basename(stim_filepath))
        stimulus_list.append(stimulus)
        stim_num += 1

    JsonWriter.generate_json_condition_file(practice_list, stimulus_list)


def main():
    make_condition_file()


if __name__ == '__main__':
    main()
