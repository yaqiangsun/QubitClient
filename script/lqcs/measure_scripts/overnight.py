

freqs = np.arange(3.42, 3.3, -0.005);
for freqi in freqs:
    sq.ramsey_df(qobjs, do_plot=False);
    dcz.initialize_gate(freqi);
    for length in range(80, 91, 1):
        c45ld5.regs.DCZGate.c45ld5.length = length;
        dcz.zpa_q_czecho(m=1, do_plot=False)
        dcz.zpa_q_czecho(m=15, dzpa_q=0.02, do_plot=False);
runner = basex.T1();
runner(q5ld5, zpa=q5ld5.freq2zpa(np.arange(3.28,3.5,0.003)),delay=10e3, rep=np.arange(50));
runner = basex.T1();
runner(q4ld5, zpa=q4ld5.freq2zpa(np.arange(3.25,3.65,0.003)),delay=10e3, rep=np.arange(50));
