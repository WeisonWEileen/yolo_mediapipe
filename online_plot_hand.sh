# cmd=(
#     "python3 mediapipe_3d.py"
#     "python3 extract_mediapipe_hand.py"
# )

# for cmd in "${cmds[@]}"
# do 
#     echo Current CMD : "$cmd"
#     gnome-terminal -- bash -c "$cmd;exec bash;"
#     sleep 0.2
# done

# cd ../..

# cmds=(
#     "python3 mediapipe_3d.py"
#     "python3 extract_mediapipe_hand.py" 
# )

# for cmd in "${cmds[@]}"
# do 
#     echo Current CMD : "$cmd"
#     gnome-terminal -- bash -c "cd $(pwd);source install/setup.bash;$cmd;exec bash;"
#     sleep 0.2
# done
python3 mediapipe_3d.py
python3 extract_mediapipe_hand.py