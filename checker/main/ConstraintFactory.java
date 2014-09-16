package lu.svv.offline.check;

import java.util.EnumMap;
import java.util.HashMap;
import java.util.Map;

import org.eclipse.emf.common.util.EList;
import lu.svv.offline.oclr.OCLRExpression;
import lu.svv.offline.oclr.PatternType;
import lu.svv.offline.oclr.ScopeType;

public class ConstraintFactory {

	private static final String GloballyTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d), subtrace:OrderedSet(trace::TraceElement) = applyScopeGlobally(self.trace, exp.scope) in checkPattern%s(subtrace, exp.pattern)";
	private static final String BeforeTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d), subtrace:OrderedSet(trace::TraceElement) = applyScopeBefore(self.trace, exp.scope) in checkPattern%s(subtrace, exp.pattern)";
	private static final String AfterTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d), subtrace:OrderedSet(trace::TraceElement) = applyScopeAfter(self.trace, exp.scope) in checkPattern%s(subtrace, exp.pattern)";
	private static final String BetweenAndTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d), subtraces:Sequence(OrderedSet(trace::TraceElement)) = applyScopeBetweenAnd(self.trace, exp.scope) in subtraces->forAll(subtrace | checkPattern%s(subtrace, exp.pattern))";
	private static final String AfterUntilTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d), subtraces:Sequence(OrderedSet(trace::TraceElement)) = applyScopeAfterUntil(self.trace, exp.scope) in subtraces->forAll(subtrace | checkPattern%s(subtrace, exp.pattern))";

	private static final String ApplyGloballyTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d) in applyScopeGlobally(self.trace, exp.scope)";
	private static final String ApplyBeforeTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d) in applyScopeBefore(self.trace, exp.scope)";
	private static final String ApplyAfterTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d) in applyScopeAfter(self.trace, exp.scope)";
	private static final String ApplyBetweenAndTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d) in applyScopeBetweenAnd(self.trace, exp.scope)";
	private static final String ApplyAfterUntilTemplate = "let exp:oclr::OCLRExpression = self.constraint.oclrExpressions->at(%d) in applyScopeAfterUntil(self.trace, exp.scope)";
	

	private static final String UniversalityLiteral = "Universality";
	private static final String ExistenceLiteral = "Existence";
	private static final String AbsenceLiteral = "Absence";
	private static final String PrecedenceLiteral = "Precedence";
	private static final String ResponseLiteral = "Response";

	private static EnumMap<ScopeType, String> propertyTemplateMap;
	private static EnumMap<ScopeType, String> scopeTemplateMap;
	private static EnumMap<PatternType, String> patternLiteralMap;
	private static ConstraintFactory factory = null;	
	
	public static ConstraintFactory init()
	{
		if (null != factory) {
			return factory;
		}
		
		propertyTemplateMap = new EnumMap<ScopeType, String>(ScopeType.class);
		propertyTemplateMap.put(ScopeType.GLOBALLY, GloballyTemplate);
		propertyTemplateMap.put(ScopeType.BEFORE, BeforeTemplate);
		propertyTemplateMap.put(ScopeType.AFTER, AfterTemplate);
		propertyTemplateMap.put(ScopeType.BETWEENAND, BetweenAndTemplate);
		propertyTemplateMap.put(ScopeType.AFTERUNTIL, AfterUntilTemplate);

		scopeTemplateMap = new EnumMap<ScopeType, String>(ScopeType.class);
		scopeTemplateMap.put(ScopeType.GLOBALLY, ApplyGloballyTemplate);
		scopeTemplateMap.put(ScopeType.BEFORE, ApplyBeforeTemplate);
		scopeTemplateMap.put(ScopeType.AFTER, ApplyAfterTemplate);
		scopeTemplateMap.put(ScopeType.BETWEENAND, ApplyBetweenAndTemplate);
		scopeTemplateMap.put(ScopeType.AFTERUNTIL, ApplyAfterUntilTemplate);
		
		patternLiteralMap = new EnumMap<PatternType, String>(PatternType.class);
		patternLiteralMap.put(PatternType.UNIVERSALITY, UniversalityLiteral);
		patternLiteralMap.put(PatternType.EXISTENCE, ExistenceLiteral);
		patternLiteralMap.put(PatternType.ABSENCE, AbsenceLiteral);
		patternLiteralMap.put(PatternType.PRECEDENCE, PrecedenceLiteral);
		patternLiteralMap.put(PatternType.RESPONSE, ResponseLiteral);

		return new ConstraintFactory();
	}
	
	public Map<String, String> createConstraint(Monitor monitor) {
		Map<String, String> constraintStringMap = new HashMap<String, String>();
		EList<OCLRExpression> oclrConstraint = monitor.getConstraint().getOclrExpressions();
		for(int i=0; i < oclrConstraint.size(); ++i) {
			OCLRExpression exp = oclrConstraint.get(i);
			String name=exp.getName();
			if(null==name) {
				name = "inv" + i;
			}
			ScopeType sType = exp.getScope().getScopeType();
			PatternType pType = exp.getPattern().getPatternType();
			constraintStringMap.put(name, String.format(propertyTemplateMap.get(sType), i+1, patternLiteralMap.get(pType)));			
		}
		return constraintStringMap;
	}
	
	public Map<String, String> createScopeQuery(Monitor monitor) {
		Map<String, String> scopeQueryStringMap = new HashMap<String, String>();
		EList<OCLRExpression> oclrConstraint = monitor.getConstraint().getOclrExpressions();
		for(int i=0; i < oclrConstraint.size(); ++i) {
			OCLRExpression exp = oclrConstraint.get(i);
			String name=exp.getName();
			if(null==name) {
				name = "inv" + i;
			}
			ScopeType sType = exp.getScope().getScopeType();
			scopeQueryStringMap.put(name, String.format(scopeTemplateMap.get(sType), i+1));			
		}
		return scopeQueryStringMap;
	}
}
