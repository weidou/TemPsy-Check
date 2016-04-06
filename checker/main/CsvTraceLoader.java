package lu.svv.offline.main;

import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.supercsv.cellprocessor.ParseInt;
import org.supercsv.cellprocessor.constraint.NotNull;
import org.supercsv.cellprocessor.ift.CellProcessor;
import org.supercsv.io.CsvBeanReader;
import org.supercsv.io.ICsvBeanReader;
import org.supercsv.prefs.CsvPreference;

import lu.svv.offline.trace.Trace;
import lu.svv.offline.trace.TraceElement;
import lu.svv.offline.trace.TraceFactory;

public class CsvTraceLoader extends CsvResource implements ResourceLoader {
	private static CsvTraceLoader instance;
	private ICsvBeanReader csvReader;
	@Override
	public Object load(String traceFilePath) {
		TraceFactory tf = TraceFactory.eINSTANCE;
		Trace trace = tf.createTrace();
		try {
			csvReader = new CsvBeanReader(new FileReader(traceFilePath), CsvPreference.STANDARD_PREFERENCE);
			
			// the header elements are used to map the values to the bean (names must match)
			final String[] header = csvReader.getHeader(true);
			
			List<TraceElement> traceElements = new ArrayList<TraceElement>();
			do {
				TraceElement next = tf.createTraceElement();
				if (csvReader.read(next, header, processors) != null) {
					traceElements.add(next);
				} else {
					break;
				};
			} while (true);
			trace.getTraceElements().addAll(traceElements);
			return trace;
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if( csvReader != null ) {
				try {
					csvReader.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return null;
	}

	@Override
	public CellProcessor[] getProcessors() {
		if (processors == null) {
			processors = new CellProcessor[] {
				new NotNull(),
				new ParseInt()
			};
		}
		return processors;
	}
	
	
	private CsvTraceLoader(){
		super();
		getProcessors();
	}
	
	public static CsvTraceLoader init() {
		if (instance == null) {
			instance = new CsvTraceLoader();
		}
		return instance;
	}

}
