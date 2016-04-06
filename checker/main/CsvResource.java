package lu.svv.offline.main;

import org.supercsv.cellprocessor.ift.CellProcessor;

public abstract class CsvResource {

	protected CellProcessor[] processors;
	
	public abstract CellProcessor[] getProcessors();
}
