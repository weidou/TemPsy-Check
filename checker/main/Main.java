package lu.svv.offline.main;

import java.io.IOException;

import org.eclipse.ocl.ParserException;

public class Main {
	private static long startTime, elapsedTime;
	private static long startLoadingTime, elapsedLoadingTime;
	private static long startCheckTime, elapsedCheckTime;
	private static long startScopeTime, elapsedScopeTime;
	private static TraceCheck tc = new TraceCheck();
	
	public static void main(String[] args) throws IOException, ParserException {

		// Load OCL functions once
		// Around 240 ms
		tc.parseOCL();

		// Experiement of checking ten properties (P3-P12) at once
		int[] lGloballyIndexes1 = {1000000,2000000,3000000,4000000,5000000,6000000,7000000,8000000,9000000,10000000};
		experiment1_1(lGloballyIndexes1);
		
		// Experiment of checking properties with globally scope
		int[] pGloballyIndexes = {1,2,3,4,5,6,7,8,9,10,11,12};
		int[] lGloballyIndexes2 = {100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000};
		experiment1(pGloballyIndexes, lGloballyIndexes2);

		// Experiment of checking properties with before scope
		int[] pBeforeIndexes = {13,14,15,16,17,18,19,20};
		int[] lBeforeIndexes = {1,2,3,4,5,6,7,8,9,10};
		String suffixBefore = "_before";
		experiment2(pBeforeIndexes, lBeforeIndexes, suffixBefore);

		// Experiment of checking properties with after scope
		int[] pAfterIndexes = {21,22,23,24,25,26,27,28,29,30,31};
		int[] lAfterIndexes = {1,2,3,4,5,6,7,8,9};
		String suffixAfter = "_after";
		experiment2(pAfterIndexes, lAfterIndexes, suffixAfter);

		// Experiment of checking properties with between-and scope (multiple sub-traces of fixed length)
		int[] pBetweenMultIndexes = {32,33,34,35};
		int[] lBetweenMultFixedLengthIndexes = {1,2,3,4,5,6,7,8,9,10};
		String suffixBetweenMultFixedLength = "_between_mult_fixed_length";
		experiment2(pBetweenMultIndexes, lBetweenMultFixedLengthIndexes, suffixBetweenMultFixedLength);

		// Experiment of checking properties with between-and scope (fixed number of sub-traces)
		int[] lBetweenMultFixedNumberIndexes = {1,2,3,4};
		String suffixBetweenMultFixedNumber = "_between_mult_fixed_number";
		experiment2(pBetweenMultIndexes, lBetweenMultFixedNumberIndexes, suffixBetweenMultFixedNumber);

		// Experiment of checking properties with between-and scope (one sub-trace, fixed length)
		int[] pBetweenOneIndexes = {36,37,38};
		int[] lBetweenOneFixedLengthIndexes = {1,2,3,4,5,6,7,8,9,10};
		String suffixBetweenOneFixedLength = "_between_one_fixed_length";
		experiment2(pBetweenOneIndexes, lBetweenOneFixedLengthIndexes, suffixBetweenOneFixedLength);
		
		// Experiment of checking properties with between-and scope (one sub-trace, various lengths)
		int[] lBetweenOneVariousLengthIndexes = {1,2,3,4,5,6,7,8,9};
		String suffixBetweenOneVariousLength = "_between_one_various_lengths";
		experiment2(pBetweenOneIndexes, lBetweenOneVariousLengthIndexes, suffixBetweenOneVariousLength);
	}
	
	public static void experiment1(int[] propertyIndexes, int[] traceIndexes) throws ParserException {
		String propertyFile = new String();
		String traceFile = new String();
		for (int p : propertyIndexes) {
			propertyFile = "p" + p + ".xmi";
			System.out.print(propertyFile + "\t");
			for (int l : traceIndexes) {
				traceFile = "p" + p + "_" + l + ".csv";
				startTime = System.currentTimeMillis();
				elapsedLoadingTime = 0;
				// Do the experiment for 100 times
				for (int i = 0; i < 100; i++) {
					startLoadingTime = System.currentTimeMillis();
					// Load the trace and property into a monitor instance 
					tc.loadMonitor(propertyFile, traceFile);
					elapsedLoadingTime += System.currentTimeMillis() - startLoadingTime;
					// Check the property on the trace
					tc.checkSingle();
					// Reset the monitor instance for memory release
					tc.resetMonitor();
				}
				elapsedTime = System.currentTimeMillis() - startTime;
			    System.out.printf("%.2f\t%.2f\t", elapsedLoadingTime/100.0, elapsedTime/100.0);
				System.gc();
			}
			System.out.println();
		}
	}

	public static void experiment1_1(int[] traceIndexes) throws ParserException {
		String propertyFile = "instances/pm.xmi";
		String traceFile = new String();

		for (int l : traceIndexes) {
			traceFile = "instances/" + l + ".csv";
			elapsedLoadingTime = 0;
			startTime = System.currentTimeMillis();
			// Do the experiment for 5 times
			for (int i = 0; i < 5; i++) {
				startLoadingTime = System.currentTimeMillis();
				// Load the trace and properties into a monitor instance
				tc.loadMonitor(propertyFile, traceFile);
				elapsedLoadingTime += System.currentTimeMillis() - startLoadingTime;
				// Check the properties on the trace
				tc.check();
				// Reset the monitor instance for memory release
				tc.resetMonitor();
			}
			elapsedTime = System.currentTimeMillis() - startTime;
		    System.out.printf("%.1f\t%.1f\t", elapsedLoadingTime/5.0, elapsedTime/5.0);
			System.gc();
		}
	}

	public static void experiment2(int[] propertyIndexes, int[] traceIndexes, String suffix) throws ParserException {
		String propertyFile = new String();
		String traceFile = new String();
		
		for (int p : propertyIndexes) {
			propertyFile = "instances/p" + p + ".xmi";
			System.out.print(propertyFile + "\t");
			for (int l : traceIndexes) {
				elapsedCheckTime = 0;
				elapsedScopeTime = 0;
				traceFile = "instances/p" + p + "_100000_" + l + suffix + ".csv";
				tc.loadMonitor(propertyFile, traceFile);
				// Do the experiment for 100 times
				for (int i = 0; i < 100; i++) {
					startCheckTime = System.currentTimeMillis();
					// Check single property over the trace
					tc.checkSingle();
					elapsedCheckTime += System.currentTimeMillis() - startCheckTime;
					startScopeTime = System.currentTimeMillis();
					// Apply the scope of the single property on the trace (part of the check procedure)
					tc.applyScopeSingle();
					elapsedScopeTime += System.currentTimeMillis() - startScopeTime;
				}
				// Print both the check time and the scope time
			    System.out.printf("%.2f\t%.2f\t", elapsedCheckTime/100.0, elapsedScopeTime/100.0);
			    tc.resetMonitor();
				System.gc();
			}
			System.out.println();
		}
	}
}
