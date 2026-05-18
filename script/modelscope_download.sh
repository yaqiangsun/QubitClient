for i in {1..100}
do
        echo "第 $i 次执行"
        # modelscope download --model MiniMax/MiniMax-M2.7 --local_dir ./MiniMaxAI/MiniMax-M2.7
        modelscope download --model moonshotai/Kimi-K2.6  --local_dir ./moonshotai/Kimi-K2.6
done