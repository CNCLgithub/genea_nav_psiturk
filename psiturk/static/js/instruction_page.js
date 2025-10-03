let init_instructions = [
    [
        "Thank you for volunteering to help out with our study.<br>" +
        "<ul>" +
        "<li>Please take a moment to adjust your seating so that you can comfortably watch the monitor and use the keyboard/mouse." +
        "<li>Close the door or do whatever is necessary to minimize disturbance during the experiment." +
        "<li>Please also take a moment to silence your phone so that you are not interrupted by any messages mid-experiment." +
        "</ul><br>" +
        "Click <b>Next</b> when you are ready to continue.",
        "left", "", false, 8
    ],
    [
        "This experiment requires you to be in <b>full screen</b> mode.<br><br>" +
        "We will switch you to full screen mode when you press <b>Next</b> below.<br><br>" +
        "Don't worry, we will return to the normal size at the end of the experiment.<br><br>" + "" +
        "Please Note: If you do need to leave in the middle, you can press the ESC key -- but please avoid this. Your responses are only useful to us if you stay in this mode until the end of the experiment.<br><br>"+
        "Click <b>Next</b> to continue.",
        "left"
    ],
    [
        "The study is designed to be <i>challenging</i>.<br><br> " +
        "Sometimes, you'll be certain about what you saw. Other times, you won't be -- that is okay! We only hope that you give your best shot at all the questions in the experiment.",
        "center"
    ],
    [
        "We know it is difficult to stay focused on the screen for too long, but we urge you to do your best.<br><br>" +
        "Thank you again for your participation in this study and for your help with our research!<br>",
        "center"
    ],
    [
        "In each trial of this experiment, you will be shown a video depicting an obstacle course. " +
        "In the video, you will see an agent standing on a \'start\' (left-most) platform and a number of other platforms in front of the agent.<br><br>" +
        "<b>Your task here will be to use the slider provided below to report how difficult it would be for the agent to go from the \'start\' (left-most) platform to the \'final\' (right-most) platform.</b><br>" +
        "<br><b>NOTES: </b><br>" +
        "Although this is a video rendered in a graphical software, <b>please assume that all the rules of physics from the real world apply</b> " +
        "-- e.g., each platform has some mass (depending on the material with which they were built) or that gravity acts in the downward direction. " +
        "<br>", "left"
    ],
    [
        "Below is an example video showing three platforms: the \'start\' platform on the left made of stone (on which the agent is standing), a wooden platform in the middle, and the \'final\' platform to the right also made of stone.<br><br>" +
        "<b>NOTE:</b> In each trial of the experiment you will see similar videos but the number, shape and material of the platforms will vary. Please report your difficulty judgment accordingly.<br><br>",
        "center", "../static/stimuli_videos/stim_wood_0.mp4"
    ],
    [
        "Let's do a small practice run to get you acquainted to the task! <br><br>" +
        "Click <b>NEXT</b> once you are ready.",
        "center"
    ],
];


class InstructionPage extends Page {
    constructor() {
        super();
        this.showInstructions();

        this.full_screen_element = document.getElementById("full_screen_element");
        this.instructions = document.getElementById("instructions");
        this.next_button = document.getElementById("next_instruction");

        this.instructions_img_div = document.getElementById("instructions_img_div");
        // this.instructions_img = document.getElementById("instructions_img");
        this.instructions_video_div = document.getElementById("instructions_video_div");
        this.instructions_video = document.getElementById("instructions_video");

        this.instruction_number = 0;
    }

    set_instruction_number(instruction_number) {
        this.instruction_number = instruction_number;
    }

    get_total_instructions() {
        return init_instructions.length;
    }

    showNextInstruction(callback) {
        this.next_button.onclick = function() {
            console.log("INFO: next button clicked.");
            callback();
        };

        if (this.instruction_number >= this.get_total_instructions()) {
            console.log("No more instructions to process.");
            return;
        }

        let instruction_array = init_instructions.slice();

        if (this.instruction_number > 1 && !Utils.isFullScreenCurrently()) {
            Utils.goFullscreen(this.full_screen_element);
        }

        InstructionPage.hideElement(this.instructions_img_div);
        InstructionPage.hideElement(this.instructions_video_div);

        if (this.instruction_number === 5 || this.instruction_number === 6) {
            InstructionPage.showElement(this.instructions_video_div);
            this.instructions_video.src = instruction_array[this.instruction_number][2];
        }

        this.instructions.innerHTML = instruction_array[this.instruction_number][0];
        this.instructions.style.textAlign = instruction_array[this.instruction_number][1];
    }

}
