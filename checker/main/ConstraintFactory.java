package lu.svv.offline.main;

import java.util.EnumMap;
import java.util.Map;
import java.util.TreeMap;

import org.eclipse.emf.common.util.EList;

import lu.svv.offline.check.Monitor;
import lu.svv.offline.tempsy.TemPsyExpression;
import lu.svv.offline.tempsy.PatternType;
import lu.svv.offline.tempsy.ScopeType;

public class ConstraintFactory {

	public static final String CheckGloballyTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d), subtrace:OrderedSet(trace::TraceElement) = applyScopeGlobally(self.trace, exp.scope) in checkPattern%s(subtrace, exp.pattern)";
	public static final String CheckBeforeTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d), subtrace:OrderedSet(trace::TraceElement) = applyScopeBefore(self.trace, exp.scope) in checkPattern%s(subtrace, exp.pattern)";
	public static final String CheckAfterTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d), subtrace:OrderedSet(trace::TraceElement) = applyScopeAfter(self.trace, exp.scope) in checkPattern%s(subtrace, exp.pattern)";
	public static final String CheckBetweenAndTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d), subtraces:Sequence(OrderedSet(trace::TraceElement)) = applyScopeBetweenAnd(self.trace, exp.scope) in subtraces->forAll(subtrace | checkPattern%s(subtrace, exp.pattern))";
	public static final String CheckAfterUntilTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d), subtraces:Sequence(OrderedSet(trace::TraceElement)) = applyScopeAfterUntil(self.trace, exp.scope) in subtraces->forAll(subtrace | checkPattern%s(subtrace, exp.pattern))";

	public static final String ApplyGloballyTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d) in applyScopeGlobally(self.trace, exp.scope)";
	public static final String ApplyBeforeTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d) in applyScopeBefore(self.trace, exp.scope)";
	public static final String ApplyAfterTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d) in applyScopeAfter(self.trace, exp.scope)";
	public static final String ApplyBetweenAndTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d) in applyScopeBetweenAnd(self.trace, exp.scope)";
	public static final String ApplyAfterUntilTemplate = "let exp:tempsy::TemPsyExpression = self.properties.temPsyExpressions->at(%d) in applyScopeAfterUntil(self.trace, exp.scope)";
	
	public static final String GloballyLiteral = "Globally";
	public static final String BeforeLiteral = "Before";
	public static final String AfterLiteral = "After";
	public static final String BetweenandLiteral = "BetweenAnd";
	public static final String AfteruntilLiteral = "AfterUntil";
	
	public static final String UniversalityLiteral = "Universality";
	public static final String ExistenceLiteral = "Existence";
	public static final String AbsenceLiteral = "Absence";
	public static final String PrecedenceLiteral = "Precedence";
	public static final String ResponseLiteral = "Response";

	private static EnumMap<ScopeType, String> checkTemplateMap;
	private static EnumMap<ScopeType, String> applyScopeTemplateMap;
	private static EnumMap<ScopeType, String> scopeLiteralMap;
	private static EnumMap<PatternType, String> patternLiteralMap;
	private static ConstraintFactory factory = null;	
	
	public static ConstraintFactory init()
	{
		if (null != factory) {
			return factory;
		}
		
		checkTemplateMap = new EnumMap<ScopeType, String>(ScopeType.class);
		checkTemplateMap.put(ScopeType.GLOBALLY, CheckGloballyTemplate);
		checkTemplateMap.put(ScopeType.BEFORE, CheckBeforeTemplate);
		checkTemplateMap.put(ScopeType.AFTER, CheckAfterTemplate);
		checkTemplateMap.put(ScopeType.BETWEENAND, CheckBetweenAndTemplate);
		checkTemplateMap.put(ScopeType.AFTERUNTIL, CheckAfterUntilTemplate);
		
		applyScopeTemplateMap = new EnumMap<ScopeType, String>(ScopeType.class);
		applyScopeTemplateMap.put(ScopeType.GLOBALLY, ApplyGloballyTemplate);
		applyScopeTemplateMap.put(ScopeType.BEFORE, ApplyBeforeTemplate);
		applyScopeTemplateMap.put(ScopeType.AFTER, ApplyAfterTemplate);
		applyScopeTemplateMap.put(ScopeType.BETWEENAND, ApplyBetweenAndTemplate);
		applyScopeTemplateMap.put(ScopeType.AFTERUNTIL, ApplyAfterUntilTemplate);
		
		scopeLiteralMap = new EnumMap<ScopeType, String>(ScopeType.class);
		scopeLiteralMap.put(ScopeType.GLOBALLY, GloballyLiteral);
		scopeLiteralMap.put(ScopeType.BEFORE, BeforeLiteral);
		scopeLiteralMap.put(ScopeType.AFTER, AfterLiteral);
		scopeLiteralMap.put(ScopeType.BETWEENAND, BetweenandLiteral);
		scopeLiteralMap.put(ScopeType.AFTERUNTIL, AfteruntilLiteral);
		
		patternLiteralMap = new EnumMap<PatternType, String>(PatternType.class);
		patternLiteralMap.put(PatternType.UNIVERSALITY, UniversalityLiteral);
		patternLiteralMap.put(PatternType.EXISTENCE, ExistenceLiteral);
		patternLiteralMap.put(PatternType.ABSENCE, AbsenceLiteral);
		patternLiteralMap.put(PatternType.PRECEDENCE, PrecedenceLiteral);
		patternLiteralMap.put(PatternType.RESPONSE, ResponseLiteral);

		return new ConstraintFactory();
	}
	
	public String createInvariant(TemPsyExpression exp) {
		ScopeType sType = exp.getScope().getScopeType();
		PatternType pType = exp.getPattern().getPatternType();
		return String.format(checkTemplateMap.get(sType), 1, patternLiteralMap.get(pType));
	}
	
	public String createScopeQuery(TemPsyExpression exp) {
		ScopeType sType = exp.getScope().getScopeType();
		return String.format(applyScopeTemplateMap.get(sType), 1);
	}
	
	public Map<String, String> createInvariants(Monitor monitor) {
		Map<String, String> invariantStringMap = new TreeMap<String, String>();
		EList<TemPsyExpression> temPsyProperties = monitor.getProperties().getTemPsyExpressions();
		for(int i=0; i < temPsyProperties.size(); ++i) {
			TemPsyExpression exp = temPsyProperties.get(i);
			String name=exp.getName();
			if(null==name) {
				name = "TemPsy" + i;
			}
			ScopeType sType = exp.getScope().getScopeType();
			PatternType pType = exp.getPattern().getPatternType();
			invariantStringMap.put(name, String.format(checkTemplateMap.get(sType), i+1, patternLiteralMap.get(pType)));			
		}
		return invariantStringMap;
	}
	
	public Map<String, String> createScopeQuery(Monitor monitor) {
		Map<String, String> scopeQueryStringMap = new TreeMap<String, String>();
		EList<TemPsyExpression> temPsyProperties = monitor.getProperties().getTemPsyExpressions();
		for(int i=0; i < temPsyProperties.size(); ++i) {
			TemPsyExpression exp = temPsyProperties.get(i);
			String name=exp.getName();
			if(null==name) {
				name = "TemPsy" + i;
			}
			ScopeType sType = exp.getScope().getScopeType();
			scopeQueryStringMap.put(name, String.format(applyScopeTemplateMap.get(sType), i+1));			
		}
		return scopeQueryStringMap;
	}
}
